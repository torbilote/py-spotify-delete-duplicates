from app import utils as utils

# add your playlists
playlists = {
    "main_stage": "0834B53OKVRls7gMuDwmak",
    "old_stage": "116x1msBQ3D1snxMJi7hUP",
    "green_stage": "4NECTGO4FlA8cElx9v0UlN",
}

if __name__ == "__main__":

    access_token = utils.get_access_token()

    duplicates = dict()

    for playlist_name, playlist_id in playlists.items():
        tracks = utils.get_playlist_tracks(playlist_id, access_token)
        duplicates[playlist_name] = utils.find_duplicates(tracks, access_token)
        utils.export_to_json_file(duplicates)

        # uncomment in order to delete duplicates from the playlists
        # utils.delete_duplicates_from_playlist(duplicates.get(playlist_name), playlist_id, access_token)