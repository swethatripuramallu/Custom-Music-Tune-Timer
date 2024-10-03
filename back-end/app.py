from flask import Flask, request, redirect, session, jsonify
import requests
import base64
import urllib.parse
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Ensure the session is configured

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

def get_auth_url(client_id, redirect_uri):
    scopes = 'user-read-recently-played user-library-read'
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
        print("Authorization code not found")  # Debug: Print error
        return jsonify({"error": "Authorization code not found"}), 400
    
    print(f"Authorization Code: {code}")  # Debug: Print authorization code
    
    token_data = get_token_data(CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI)
    if 'error' in token_data:
        print(f"Error in token data: {token_data['error']}")  # Debug: Print error
        return jsonify({"error": token_data['error']}), 400

    session['access_token'] = token_data['access_token']
    session['refresh_token'] = token_data['refresh_token']
    session['expires_at'] = datetime.now(timezone.utc) + timedelta(seconds=token_data['expires_in'])
    
    print(f"Access Token: {session['access_token']}")  # Debug: Print access token
    print(f"Refresh Token: {session['refresh_token']}")  # Debug: Print refresh token
    print(f"Expires At: {session['expires_at']}")  # Debug: Print expires at
    
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
            print(f"Failed to refresh token: {response.status_code}")  # Debug: Print status code
            print(f"Response Content: {response.content}")  # Debug: Print response content
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
        print(f"Failed to fetch liked songs: {response.status_code}")  # Debug: Print status code
        print(f"Response Content: {response.content}")  # Debug: Print response content
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
        print(f"Failed to fetch recently played songs: {response.status_code}")  # Debug: Print status code
        print(f"Response Content: {response.content}")  # Debug: Print response content
        return jsonify({'error': 'Failed to fetch recently played songs'}), response.status_code
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port='5001', debug=True)