import json
from datetime import datetime

import requests

from app import config as cfg


def get_access_token() -> str:
    api_response = requests.post(
        url=cfg.auth_url,
        headers={**cfg.auth_headers},
        data=f"grant_type=client_credentials&client_id={cfg.client_id}&client_secret={cfg.client_secret}",
    )

    if api_response.status_code != 200:
        raise requests.ConnectionError

    return api_response.json().get("access_token")


def get_playlist_tracks(playlist_id: str, bearer_access_token: str) -> list:
    api_response = requests.get(
        url=f"{cfg.base_url}/playlists/{playlist_id}",
        headers={"Authorization": f"Bearer {bearer_access_token}"},
        params={
            "fields": "tracks.items(added_at, added_by.id, track(id, name, artists(name)))"
        },
    )

    if api_response.status_code != 200:
        raise requests.ConnectionError

    return api_response.json().get("tracks").get("items")


def find_duplicates(tracks: list[dict], bearer_access_token: str) -> list[dict]:
    unique_tracks = list()
    duplicated_tracks = list()
    user_ids = dict()

    tracks = sorted(tracks, key=lambda x: _get_datetime(x["added_at"]))

    for track in tracks:
        track_id = track.get("track").get("id")
        user_id = track.get("added_by").get("id")

        if not user_ids.get(user_id):
            user_name = _get_user_name(user_id, bearer_access_token)
            user_ids[user_id] = user_name

        if track_id not in unique_tracks:
            unique_tracks.append(track_id)

        else:
            duplicated_tracks.append(
                {
                    "artist_name": track.get("track").get("artists")[0].get("name"),
                    "track_name": track.get("track").get("name"),
                    "track_id": track_id,
                    "added_by_name": user_ids.get(user_id),
                }
            )

    return duplicated_tracks


def export_to_json_file(data: dict) -> None:
    with open("output.json", "w", encoding="utf-8") as output_file:
        output_file.write(json.dumps(data, ensure_ascii=False, indent=2))


def _get_user_name(user_id: str, bearer_access_token: str) -> str:
    api_response = requests.get(
        url=f"{cfg.base_url}/users/{user_id}",
        headers={"Authorization": f"Bearer {bearer_access_token}"},
    )

    if api_response.status_code != 200:
        raise requests.ConnectionError

    return api_response.json().get("display_name")


def _get_datetime(datetime_as_str: str) -> datetime:
    return datetime.strptime(datetime_as_str, "%Y-%m-%dT%H:%M:%SZ")

def delete_duplicates_from_playlist(tracks: list[dict], playlist_id: str, bearer_access_token: str) -> None:
    if not tracks:
        return

    api_response = requests.delete(
        url=f"{cfg.base_url}/playlists/{playlist_id}/tracks",
        headers={"Authorization": f"Bearer {bearer_access_token}"},
        data= {
            "tracks": [
                {
                    "uri": f"spotify:track:{track.get('track_id')}"
                }
                for track in tracks
            ]
        }
    )

    if api_response.status_code != 200:
        raise requests.ConnectionError