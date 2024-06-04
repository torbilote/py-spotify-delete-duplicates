import os

from dotenv import load_dotenv

load_dotenv()

auth_url = "https://accounts.spotify.com/api/token"
auth_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

base_url = "https://api.spotify.com/v1"

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

playlists = {
    "main_stage": "0834B53OKVRls7gMuDwmak",
    "old stage": "116x1msBQ3D1snxMJi7hUP",
    "green stage": "4NECTGO4FlA8cElx9v0UlN",
}
