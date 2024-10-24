# Import all necessary libraries
import base64
import os
import requests 
import urllib.parse
from flask import Flask, redirect, request, jsonify, session
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS
from flask_caching import Cache

# Load environement variables
load_dotenv()

# Initialize Flask app and configure CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')

# Spotify API credentials and URLs
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

""" ALL APPLICATION ROUTES """

# Redirect to Spotify Login Page, 
@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-read-recently-played user-library-read user-top-read'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }
    # Make a get request to user's data, also encoded the users params
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

# Scenario for when the user fails to login successfully
@app.route('/callback')
def callback():
    # Checks if spotify outputs an error
    if 'error' in request.args:
        return jsonify({"error": request.args['error']}) 
   
    # Assume the spotify didn't throw an error
    if 'code' in request.args:
        # Build up a request body to acquire access token
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    response = requests.post(TOKEN_URL, data=req_body) # Sent the body off to spotify
    token_info = response.json() # Response from spotify

    # Keep this information at all times
    session['access_token'] = token_info['access_token'] # Access token only lasts for 1 day 
                                                         # Will need experiation and refresh token also
    session['refresh_token']= token_info['refresh_token']

    session['expires_at']= datetime.now().timestamp() + token_info['expires_in']


    return jsonify(token_info)
    # return  redirect('filter-songs/duration') # Retrieves all the playlists

# Generates a refresh token to keep the user logged in
@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session: # Check the refresh token
        return redirect('/login')
    
    if datetime.now().timestamp() . session['expires_at']:
        # Make a request to get a fresh access token
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    
    response = request.post(TOKEN_URL, data= req_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

    return jsonify(new_token_info)
    # return redirect('filter-songs/duration')

@app.route('/song-recs', methods=['GET'])
def get_recommendations(access_token, happy, sad, dance, productive):
    # Check if the user is authenticated
    # receives booleans for the mood of the user
    if 'access_token' not in session:
        return jsonify({'error': 'User not authenticated'}), 401
    
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    # Fetch user's mood
    genres= []
    if (happy):
        genres.append('happy')
    if (sad):
        genres.append('sad')
    if (dance):
        genres.append('dance')
    if (productive):
        genres.append('study')

    # Fetch recommendations based on the user's mood
    url = '{API_BASE_URL}recommendations?limit=100&seed_genres={genres}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        recommendations = response.json().get('tracks', [])
    else:
        return jsonify({'error': 'Failed to fetch recommendations'}), response.status_code

# Parses through the user's recently played, liked songs, and recommended songs
@app.route('/parse')
def parse_songs(happy, sad, dance, productive):
    if 'recommended-songs' not in session:
        get_recommendations(happy, sad, dance, productive)

    tracks = [] 
    
    tracks_get_recommendations = session['recommended-songs']
   
    # Initialize an empty set to keep track of already seen tracks (to avoid duplicates)
    seen_tracks = set()

    for item in tracks_get_recommendations:
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

    return tracks

# Creates a playlist based on the user's mood and desired playlist length
@app.route('/create-playlist', methods=['POST, GET'])
def create_playlist():
        data = request.get_json()  # Parse incoming JSON request body
        print('Received data:', data)
       
        length = int(data.get('length'))
        # cache.set('length',length)
        happy = data.get('happy')
        sad = data.get('sad')
        dance = data.get('dance')
        productive = data.get('productive')

        tracks = parse_songs(happy, sad, dance, productive)
        filtered_tracks = filterSongsByDuration(tracks, length)

        # Send a response back to the client
        return jsonify({"message": "Playlist creation successful", "data": filtered_tracks})

# Filters songs based on the user's desired playlist length
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

            if new_sum <= duration:
                # If this sum is not already in the dictionary, add it with its corresponding subset
                if new_sum not in achievable_sums:
                    achievable_sums[new_sum] = achievable_sums[current_sum] + [track]
    
    # Find the closest sum that is not greater than the target
    closest_sum = max(achievable_sums.keys())
    
    return achievable_sums[closest_sum]  

# Filter songs based on the user's desired playlist length
@app.route('/duration')
def run_duration():
    tracks = parse_songs()
    return filterSongsByDuration(tracks, cache.get('length'))

# Run the Flask app
if __name__ == '__main__':
    app.run(port = "5001", debug=True) #any changes we make in the code the 
                                        #server will automatically refresh
