import base64
import os
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
    
    recommendedTracks = recommended.get('tracks', [])
    # Initialize an empty set to keep track of already seen tracks (to avoid duplicates)
    #seen_tracks = set()

    for item in recommendedTracks:
        track_name = item['name']
        artists = item.get('artists', [])
        artist_names = ", ".join([artist.get('name', 'Unknown Artist') for artist in artists])
        duration = item['duration_ms']
        track_id = item.get('id', "Unknown ID")

        song_info = {
            'track_name' : track_name,
            'artist_name': artist_names,
            'duration': duration,
            'track_id': track_id
        }

        tracks.append(song_info)

        #seen_tracks.add(track_key)

    
    return tracks

def filterSongsByDuration(tracks: list, duration: float):
        #sort tracks by duration in descending order
        sorted_tracks = sorted(tracks, key=lambda x: x['duration'], reverse = True) 

        selected_tracks = []
        current_duration = 0

        for track in sorted_tracks:
            if current_duration + track['duration'] <= duration:
                selected_tracks.append(track)
                current_duration += track['duration']

            if current_duration >= duration:
                break 

        return selected_tracks           



# Function to fetch Spotify data based on user input
def get_spotify_data(length, happy, sad, dance, productive):
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope='user-library-read user-read-recently-played playlist-modify-public user-top-read',
        cache_path='.cache'
    ))
    
    # Modify recommendations based on moods or user input (happy, sad, dance, etc.)
    if happy:
        seed_genres = ['happy']
    elif sad:
        seed_genres = ['sad']
    elif dance:
        seed_genres = ['dance']
    elif productive:
        seed_genres = ['classical']
    else:
        seed_genres = ['pop']
    
    # Seeds based on user tracks and user artists
    top_tracks = sp.current_user_top_tracks(limit=2)
    seed_tracks = [track['id'] for track in top_tracks['items']]

    top_artists = sp.current_user_top_artists(limit=3)
    seed_artists = [artist['id'] for artist in top_artists['items']]

    # Fetch recommended songs based on mood
    recommendations = sp.recommendations(seed_tracks=seed_tracks, seed_artists=seed_artists, limit=100)

    tracks = parse_songs(recommendations)
    filtered_songs = filterSongsByDuration(tracks, length)
    
    # Create a new playlist
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name="Tune Timer Playlist", public=True,
                                       description="A playlist created based on your selected mood and duration.")
    # Get the track URIs for the filtered songs
    track_uris = [f"spotify:track:{track['track_id']}" for track in filtered_songs]

    # Add tracks to the new playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

    # Return the playlist information along with track data
    response_data = {
        'playlist_id': playlist['id'],
        'playlist_url': playlist['external_urls']['spotify'],
        'tracks': filtered_songs
    }

    return response_data


@app.route('/callback')
def callback():
    return "Authentication Sucessful!"

# Flask route to handle playlist creation
@app.route('/create-playlist', methods={'POST'})
def create_playlist():
    data = request.get_json()  # Parse incoming JSON request body
    print('Received data:', data)
   
    length = int(data.get('length')) * 60000
    happy = data.get('happy')
    sad = data.get('sad')
    dance = data.get('dance')
    productive = data.get('productive')

    # Get Spotify data based on mood
    spotify_data = get_spotify_data(length, happy, sad, dance, productive)
    
    tracks = spotify_data['tracks']

   # print("Spotify Data:", spotify_data)
    for track in tracks:
        track_name = track['track_name']
        track_artist = track['artist_name']
        print(f"{track_name} by {track_artist}")
       
    
    # # Create a response including Spotify data
    # response = {
    #   "message": "Playlist creation successful",
    #    "data": {
    #        "length": length,
    #        "happy": happy,
    #        "sad": sad,
    #        "dance": dance,
    #        "productive": productive,
    #        "spotify_data": spotify_data
    #    }
    # }
    
    
    return jsonify(spotify_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 
