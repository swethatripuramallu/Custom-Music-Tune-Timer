import requests
import base64
import os
import urllib.parse
from flask import Flask, redirect, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH_URL = 'https://accounts.spotify.com/authorize'
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
        return jsonify({"error": "Authorization code not found"}), 400
    token_data = get_token_data(CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI)
    session['token_data'] = token_data
    return jsonify(token_data)

if __name__ == '__main__':
    app.run(debug=True)