import requests
from flask import Flask, session, redirect, jsonify, Blueprint
from datetime import datetime

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

filterSongs_bp = Blueprint("filterSongs", __name__)

@filterSongs_bp.route('/playlists')
def get_playlists():
    if 'access_token' not in session: #check the access token 
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token') #automatically refresh it for them so we don't interrupt the user interface

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers = headers)
    playlists = response.json()

    return jsonify(playlists)



@filterSongs_bp.route('/duration')
def test():
    return 'Reached filtered songs'

# def filterSongsByDuration(song_database: List[dict], min_duration: float, max_duration: float):
#     '''
#         Inputs:
#         - song_database: List[dict] specifies that song_database is a list of dictionaries 
#         (assuming each song is represented as a dictionary with details like title, artist, and duration).
#         - min_duration and max_duration is the range in which the playlist can fall in. e.g. a playlist is 15 minutes 
#         we might want the playlist to fall between 14 1/2 to 15 1/2 minutes

#     '''

#     return 'Reached FilteredSongs'


