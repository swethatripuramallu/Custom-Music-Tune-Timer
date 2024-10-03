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

    response = requests.get(API_BASE_URL + 'me/player/recently-played', headers = headers, params={'limit': 50, '0ffset': 0})
    # tracks = response.json()

    # Parse the JSON response to get track details
    tracks_data = response.json().get('items', [])
    tracks = []

    for item in tracks_data:
        track_info = {
                "Song Name": item["track"]["name"],
                "Artist Name": item["track"]["album"]["artists"][0]["name"],
                "Duration (ms)": item["track"]["duration_ms"],
                "Spotify Link": item["track"]["external_urls"]["spotify"]
        }
        tracks.append(track_info)

    return tracks  # Return the list of track details for further use/display


def filterSongsByDuration(tracks: list, min_duration: float, max_duration: float):
    return [track for track in tracks if min_duration <= track["Duration (ms)"] <= max_duration]

@filterSongs_bp.route('/duration')
def run():
    tracks = get_playlists()
    return filterSongsByDuration(tracks, 229179, 321225)

