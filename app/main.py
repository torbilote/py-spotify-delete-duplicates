import requests
from app import config as cfg
import json

initial_request = requests.post(
    url=cfg.auth_url,
    headers=cfg.auth_headers,
    data=f"grant_type=client_credentials&client_id={cfg.client_id}&client_secret={cfg.client_secret}"
)

bearer_access_token = initial_request.json().get('access_token')

#1 get_specific_playlist
get_playlist = requests.get(
    url=f"{cfg.base_url}/playlists/{cfg.playlist_id}",
    headers={ "Authorization": f"Bearer {bearer_access_token}" },
    params={ "fields": "tracks.items(track(id))" }
)

with open('output_1.json', 'w') as output_file:
    output_file.write(get_playlist.text)

#2 iterate_through_playlist_and_identify_duplicated_items
tracks = get_playlist.json().get('tracks').get('items')

unique_tracks = list()
duplicated_tracks = list()

for track in tracks:
    track_id = track.get('track').get('id')

    if not track_id:
        continue

    if track_id not in unique_tracks:
        unique_tracks.append(track_id)
    else:
        duplicated_tracks.append(track_id)

with open('output_2.json', 'w') as output_file:
    output_file.write(json.dumps(duplicated_tracks))

#3 save_duplicated_items_to_file
items = dict()

for index, duplicate in enumerate(duplicated_tracks):
    item = requests.get(
        url=f"{cfg.base_url}/tracks/{duplicate}",
        headers={ "Authorization": f"Bearer {bearer_access_token}" },
    )

    if item.status_code == 200:
        item = item.json()

        items[index] = {
            "first_artist_name": item.get('artists')[0].get('name'),
            "track_name": item.get('name'),
        }

with open('output_3.json', 'w') as output_file:

    output_file.write(json.dumps(items, ensure_ascii=False))
