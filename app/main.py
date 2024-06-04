from app import config as cfg
from app import utils as utils

if __name__ == "__main__":
    access_token = utils.get_access_token()

    duplicates = dict()

    for playlist_name, playlist_id in cfg.playlists.items():
        tracks = utils.get_playlist_tracks(playlist_id, access_token)
        duplicates[playlist_name] = utils.find_duplicates(tracks, access_token)
        utils.export_to_json_file(duplicates)

        # uncomment below in order to delete duplicates from the playlists
        # utils.delete_duplicates_from_playlist(duplicates.get(playlist_name), playlist_id, access_token)