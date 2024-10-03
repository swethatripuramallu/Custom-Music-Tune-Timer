from flask import Flask, request, redirect, session, jsonify
import requests
import base64
import urllib.parse
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Ensure the session is configured

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

def get_auth_url(client_id, redirect_uri):
    scopes = 'user-read-recently-played user-library-read user-top-read'
    auth_url = (
        'https://accounts.spotify.com/authorize?'
        f'client_id={client_id}'
        f'&response_type=code'
        f'&redirect_uri={urllib.parse.quote(redirect_uri)}'
        f'&scope={urllib.parse.quote(scopes)}'
    )
    return auth_url

def get_token_data(client_id, client_secret, code, redirect_uri):
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    token_headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    token_response = requests.post(TOKEN_URL, data=token_data, headers=token_headers)
    return token_response.json()

@app.route('/login')
def login():
    auth_url = get_auth_url(CLIENT_ID, REDIRECT_URI)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code is None:
        return jsonify({"error": "Authorization code not found"}), 400
        
    token_data = get_token_data(CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI)
    if 'error' in token_data:
        return jsonify({"error": token_data['error']}), 400

    session['access_token'] = token_data['access_token']
    session['refresh_token'] = token_data['refresh_token']
    session['expires_at'] = datetime.now(timezone.utc) + timedelta(seconds=token_data['expires_in'])

    return redirect('/')

def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now(timezone.utc) >= session['expires_at']:
        auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        token_data = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token']
        }
        token_headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(TOKEN_URL, data=token_data, headers=token_headers)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to refresh token'}), response.status_code
        
        new_token_data = response.json()
        session['access_token'] = new_token_data['access_token']
        session['expires_at'] = datetime.now(timezone.utc) + timedelta(seconds=new_token_data['expires_in'])
    
    return session['access_token']

@app.route('/liked-songs')
def liked_songs():
    access_token = refresh_token()
    if not access_token:
        return redirect('/login')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(f'{API_BASE_URL}me/tracks', headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch liked songs'}), response.status_code
    
    return jsonify(response.json())

@app.route('/recently-played')
def recently_played():
    access_token = refresh_token()
    if not access_token:
        return redirect('/login')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(f'{API_BASE_URL}me/player/recently-played', headers=headers)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch recently played songs'}), response.status_code
    
    return jsonify(response.json())

@app.route('/song-recs', methods=['GET'])
def get_recommendations():
    access_token = refresh_token()
    if not access_token:
        return redirect('/login')

    headers = {
        'Authorization': f'Bearer {access_token}'
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

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port='5001', debug=True)