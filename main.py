import requests
import base64
import os

from dotenv import load_dotenv
load_dotenv()

# My Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Spotify token URL
TOKEN_URL = "https://accounts.spotify.com/api/token"

# Encode credentials
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

# Request access token
response = requests.post(
    TOKEN_URL,
    headers={"Authorization": f"Basic {auth_header}"},
    data={"grant_type": "client_credentials"},
)

# Get token
token_data = response.json()
ACCESS_TOKEN = token_data["access_token"]
print("Access Token:", ACCESS_TOKEN)

def get_artist_id(artist_name, access_token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    try:
        artist = data['artists']['items'][0]
        return artist['id'], artist['name']
    except (IndexError, KeyError):
        print("Artist not found.")
        return None, None

ARTIST_ID, ARTIST_NAME = get_artist_id("Electric Six", ACCESS_TOKEN)
print(f"{ARTIST_NAME}'s Spotify ID is {ARTIST_ID}")


# ARTIST_ID = "36QJpDe2go2KgaRleHCDTp"  # Led Zeppelin's ID
SPOTIFY_API_URL = f"https://api.spotify.com/v1/artists/{ARTIST_ID}"

response = requests.get(
    SPOTIFY_API_URL,
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
)

artist_data = response.json()
print("Artist Name:", artist_data["name"])
print("Popularity:", artist_data["popularity"])
print("Genres:", ", ".join(artist_data["genres"]))
print()
print(artist_data)
print()

COUNTRY_CODE = "JP"  # Japan
TOP_TRACKS_URL = f"https://api.spotify.com/v1/artists/{ARTIST_ID}/top-tracks?market={COUNTRY_CODE}"

response = requests.get(
    TOP_TRACKS_URL,
    headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
)

tracks = response.json()["tracks"]
for track in tracks:
    print(track["name"], "-", track["popularity"])
