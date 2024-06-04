from app import config as cfg
from app import utils as utils

if __name__ == "__main__":
    access_token = utils.get_access_token()

    duplicates = dict()

    for playlist_name, playlist_id in cfg.playlists.items():
        tracks = utils.get_playlist_tracks(playlist_id, access_token)
        duplicated_tracks_list = utils.find_duplicates(tracks, access_token)
        duplicates[playlist_name] = duplicated_tracks_list
        utils.export_to_json_file(duplicates)


