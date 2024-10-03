import requests
from flask import Flask, session, redirect, jsonify, Blueprint
from datetime import datetime
from itertools import combinations

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

def filterSongsByDuration(tracks: list, duration: float):
    """
    Finds a subset of tracks whose total duration is closest to the given target value without exceeding it.

    Parameters:
    tracks (list): A list of track dictionaries containing information about each track.
    duration (float): The target duration value in milliseconds.

    Returns:
    list: The subset of tracks that result in the closest total duration.
    """
    # Initialize a dictionary to store achievable sums and corresponding subsets
    achievable_sums = {0: []}  # Key is the sum, value is the subset list
    
    # Iterate through each track in the list
    for track in tracks:
        track_duration = track["Duration (ms)"]

        # Copy existing achievable sums to avoid modifying the dictionary while iterating
        current_sums = list(achievable_sums.keys())
        
        for current_sum in current_sums:
            new_sum = current_sum + track_duration
            
            # Only add the new sum if it does not exceed the target duration
            if new_sum <= duration:
                # If this sum is not already in the dictionary, add it with its corresponding subset
                if new_sum not in achievable_sums:
                    achievable_sums[new_sum] = achievable_sums[current_sum] + [track]
    
    # Find the closest sum that is not greater than the target
    closest_sum = max(achievable_sums.keys())
    
    return achievable_sums[closest_sum]  # Return the subset of tracks that result in the closest total duration


@filterSongs_bp.route('/duration')
def run():
    tracks = get_playlists()
    return filterSongsByDuration(tracks, 600000)

