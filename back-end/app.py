# Import all necessary libraries
import base64
import os
import requests 
import urllib.parse
from flask import Flask, redirect, request, jsonify, session
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS

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
        # Force the user to login everytime into application by setting show_dialog true 
        # Will make debugging easier for local server purpose, can change at the end
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

# Fetches some of the user's liked songs
@app.route('/liked-songs')
def liked_songs():
    if 'access_token' not in session: 
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(f'{API_BASE_URL}me/tracks', headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch liked songs'}), response.status_code
    
    session['liked-songs'] = response.json().get('items', [])
    return jsonify(response.json())

# Fetches some of the user's recently played songs
@app.route('/recently-played')
def recently_played():
    if 'access_token' not in session: 
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(f'{API_BASE_URL}me/player/recently-played', headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch recently played songs'}), response.status_code
    
    session['recently-played'] = response.json().get('items', [])
    return jsonify(response.json())

# Fetches song recommendations based on the user's top artists and tracks
@app.route('/song-recs', methods=['GET'])
def get_recommendations():
    if 'access_token' not in session: 
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    # Get user's top artists
    try:
        top_artists_response = requests.get(f'{API_BASE_URL}me/top/artists', headers=headers, params={'limit': 5})
        top_artists_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top artists: {e}")
        return jsonify({'error': 'Failed to get top artists'}), 500

    top_artists = top_artists_response.json().get('items', [])
    seed_artists = [artist['id'] for artist in top_artists[:2]]  # Limit to 2 seeds

    # Get user's top tracks
    try:
        top_tracks_response = requests.get(f'{API_BASE_URL}me/top/tracks', headers=headers, params={'limit': 5})
        top_tracks_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching top tracks: {e}")
        return jsonify({'error': 'Failed to get top tracks'}), 500

    top_tracks = top_tracks_response.json().get('items', [])
    seed_tracks = [track['id'] for track in top_tracks[:3]]  # Limit to 3 seeds

    if not seed_artists and not seed_tracks:
        return jsonify({'error': 'No seeds available for recommendations'}), 400

    # Use top artists and tracks as seeds for recommendations
    params = {
        'limit': 10,  # Number of recommendations to return
        'seed_artists': ','.join(seed_artists),
        'seed_tracks': ','.join(seed_tracks)
    }

    try:
        response = requests.get(f'{API_BASE_URL}recommendations', headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching recommendations: {e}")
        return jsonify({'error': 'Failed to get recommendations'}), 500

    session['recommended-songs'] = response.json().get('items', [])
    return jsonify(response.json())

# Filter songs by moods
def filter_songs_by_mood(access_token):
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    # Fetching the user's recently played tracks
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{API_BASE_URL}me/player/recently-played', headers=headers)
    if response.status_code == 200:
        mood_recently_played = response.json().get('items', [])
    else:
        return jsonify({'error': 'Failed to fetch recently played songs'}), response.status_code

    # Fetching the user's liked / saved tracks
    response = requests.get(f'{API_BASE_URL}me/tracks', headers=headers)
    if response.status_code == 200:
        mood_liked_songs = response.json().get('items', [])
    else:
        return jsonify({'error': 'Failed to fetch liked songs'}), response.status_code

    # Fetching song recommendations based on the user's top artists and tracks
    mood_recommendations = get_recommendations()

    # Fetching audio features for each track
    all_mood_tracks = mood_recently_played + mood_liked_songs + session.get('recommended-songs', [])
    track_ids = [track['track']['id'] for track in all_mood_tracks if 'track' in track]

    # Filter tracks based on moods - using valence factors
    if track_ids:
        response = requests.get(f'https://api.spotify.com/v1/audio-features', headers=headers, params={'ids': ','.join(track_ids)})
        if response.status_code != 200:
            return jsonify({'error': 'Failed to fetch audio features'}), response.status_code

        audio_features = response.json().get('audio_features', [])
        # Return HAPPY filtered tracks
        happy_tracks = [track for track in audio_features if track['valence'] > 0.7]

        return jsonify(happy_tracks)
    else:
        return jsonify({'error': 'No tracks found'})

# Mood route for user's playlist if they opt for a mood based playlist
@app.route('/mood', methods=['GET'])
def mood():
    access_token = session.get('access_token')  # Fetch access token from the session
    if not access_token:
        return jsonify({'error': 'Access token missing'}), 401
    
    return mood(access_token)

# Parses through the user's recently played, liked songs, and recommended songs
@app.route('/parse')
def parse_songs():
    if 'recently-played' not in session:
        recently_played()
    if 'liked-songs' not in session:
        liked_songs()
    if 'recommended-songs' not in session:
        get_recommendations()

    tracks = []
    
    tracks_data = session['recently-played']
    tracks_liked_songs = session['liked-songs']
    tracks_get_recommendations = session['recommended-songs']
   
    # Initialize an empty set to keep track of already seen tracks (to avoid duplicates)
    seen_tracks = set()

    #  Appends and parses through all the json data and formulates a track data table with all the correct parameters
    for item in tracks_data:
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

    for item in tracks_liked_songs:
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

# Filters songs based on the target duration
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

# Sets playlist duration based on what the user desires in milliseconds
@app.route('/duration')
def run_duration():
    tracks = parse_songs()
    return filterSongsByDuration(tracks, 900000)

# Run the Flask app
if __name__ == '__main__':
    app.run(port = "5001", debug=True) #any changes we make in the code the 
                                        #server will automatically refresh


