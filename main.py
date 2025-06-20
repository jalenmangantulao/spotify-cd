import requests
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

import json
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'https://127.0.0.1:3000/callback' or 'https://127.0.0.1:3000/callback' #my case is 'http://localhost:3000/callback'
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

    token = spotify.fetch_token(TOKEN_URL, auth=auth_info, authorization_response=code)

    r = spotify.get('https://api.spotify.com/v1/me')
    print(r.content)

login()
    