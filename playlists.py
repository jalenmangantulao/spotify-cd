import requests
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

import json
import os
import pprint

from dotenv import load_dotenv

#global spotify

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

load_dotenv()

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'https://127.0.0.1:3000/callback'
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('SECRET')
SCOPE = [
    "user-read-email",
    "playlist-read-collaborative"
]
TOKEN = None
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#auth_info = {'grant_type' : 'authorization_token',
#             'client_id' : CLIENT_ID,
#             'client_secret' : CLIENT_SECRET}
auth_info = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

def get_token():
    x = requests.post(TOKEN_URL, auth_info, headers)
    r = json.loads(x.text)
    TOKEN = r['access_token']

def login():
    spotify = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = spotify.authorization_url(AUTH_URL)
    print(authorization_url)
    code = input()
    token = spotify.fetch_token(TOKEN_URL, auth=auth_info, authorization_response=code, state=state)
    return spotify

def test(spotify):
    user = spotify.get('https://api.spotify.com/v1/me')
    user_json = json.loads(user.content)
    USER_ID = user_json['id']
    playlists = spotify.get(f'https://api.spotify.com/v1/users/{USER_ID}/playlists')
    parsed = json.loads(playlists.content)
    for i in parsed.get('items'):
        if i.get('external_urls'):
            if i['owner']['id'] == USER_ID:
                print(f"Playlist name: {i['name']}, Playlist ID: {i['id']}, Tracks href: {i['tracks']['href']}")

        first_track_list = spotify.get(i['tracks']['href'])
        tracks_json = json.loads(first_track_list.content)
        for j in tracks_json.get('items'):
            if j.get('track'):
                artists = j['track']['artists']
                artists_names = [a['name'] for a in artists]
                names = ",".join(artists_names)
                track_name = j['track']['name']
                print(f"{track_name} by {names}")
s = login()
test(s)

    