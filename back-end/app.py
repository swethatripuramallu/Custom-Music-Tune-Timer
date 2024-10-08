import base64
import os
import requests 
import urllib.parse
from flask import Flask, redirect, request, jsonify, session
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS

# load environement variables
load_dotenv()

app = Flask(__name__)

CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

#Redirect to Spotify Login Page, Need to declare scope/permissions
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
        # to make debugging easier for local server purpose, can change at the end
    }
    #make a get request to user's data, also encoded the users params
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)



#Scenario for when the user fails to login successfully
@app.route('/callback')
def callback():
    #check if spotify threw an error
    if 'error' in request.args:
        return jsonify({"error": request.args['error']}) #just throwing back and error 404 page
   
    #assume the spotify didn't throw an error
    if 'code' in request.args:
        #build up a request body to acquire access token
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    response = requests.post(TOKEN_URL, data=req_body) #sent the body off to spotify
    token_info = response.json() #response from spotify

    #keep this information at all times
    session['access_token'] = token_info['access_token'] #access token only lasts for 1 day 
                                                             #so we need the expiration and refresh token as well
    session['refresh_token']= token_info['refresh_token']

    session['expires_at']= datetime.now().timestamp() + token_info['expires_in']


    return jsonify(token_info)
    # return  redirect('filter-songs/duration') #retrieves all the playlists


@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session: #check the refresh token
        return redirect('/login')
    
    if datetime.now().timestamp() . session['expires_at']:
        #make a request to get a fresh access token
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

@app.route('/duration')
def run_duration():
    tracks = parse_songs()
    return filterSongsByDuration(tracks, 600000)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) #any changes we make in the code the 
                                        #server will automatically refresh


