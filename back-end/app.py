import base64
import os
import requests
import urllib.parse
from flask import Flask, redirect, request, jsonify, session
#from flask_session import Session
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS
from cachelib.file import FileSystemCache
import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

# load environement variables
load_dotenv()

app = Flask(__name__)

CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')

#Flask server-side sessions (e.g., Redis, filesystem)
cache = FileSystemCache('/tmp/flask_cache')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

def parse_songs(recommended):

    tracks = []
  
    # Initialize an empty set to keep track of already seen tracks (to avoid duplicates)
    seen_tracks = set()

    for item in recommended:
        track_name = item["track"]["name"]
        artist_name = item["track"]["album"]["artists"][0]["name"]
        track_key = (track_name, artist_name)
        
        if track_key not in seen_tracks:
            track_info = {
                "Song Name": track_name,
                "Artist Name": artist_name,
                "Duration (ms)": item["track"]["duration_ms"],
                "Spotify Link": item["track"]["external_urls"]["spotify"],
                "Track ID:": item["track"]["id"]
            }
            tracks.append(track_info)
            seen_tracks.add(track_key)

    logging.info(f"Successfully parsed {len(tracks)} unique tracks.")  # Logging added here
    return tracks

def filterSongsByDuration(tracks: list, duration: float):
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
    
    return achievable_sums[closest_sum]  

# Function to fetch Spotify data based on user input
def get_spotify_data(length, happy, sad, dance, productive):
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-library-read user-read-recently-played playlist-modify-public'
    ))

    # Modify recommendations based on moods or user input (happy, sad, dance, etc.)
    if happy:
        seed_genres = ['pop', 'happy']
    elif sad:
        seed_genres = ['sad', 'blues']
    elif dance:
        seed_genres = ['dance', 'edm']
    elif productive:
        seed_genres = ['classical', 'ambient']
    else:
        seed_genres = ['pop', 'rock']

    # Fetch recommended songs based on mood
    recommendations = sp.recommendations(seed_genres=seed_genres, limit=100)

    tracks = parse_songs(recommendations)

    filtered_songs = filterSongsByDuration(recommendations, length)

    # Return the data as a dictionary
    return filtered_songs

# Flask route to handle playlist creation
@app.route('/create-playlist', methods=['POST'])
def create_playlist():
    data = request.get_json()  # Parse incoming JSON request body
    print('Received data:', data)
   
    length = int(data.get('length'))
    happy = data.get('happy')
    sad = data.get('sad')
    dance = data.get('dance')
    productive = data.get('productive')

    # Get Spotify data based on mood
    spotify_data = get_spotify_data(length, happy, sad, dance, productive)

    # Create a response including Spotify data
    response = {
        "message": "Playlist creation successful",
        "data": {
            "length": length,
            "happy": happy,
            "sad": sad,
            "dance": dance,
            "productive": productive,
            "spotify_data": spotify_data
        }
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 
