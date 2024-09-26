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


def get_auth_url(client_id, redirect_uri):
    scope = 'user-read-recently-played user-library-read'
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True
        # Force the user to login everytime into application by setting show_dialog true 
        # to make debugging easier for local server purpose, can change at the end
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return auth_url

  
def get_token_data(client_id, client_secret, code, redirect_uri):
   #build up a request body to acquire access token
    req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
    }
    response = requests.post(TOKEN_URL, data=req_body) #sent the body off to spotify
    token_info = response.json()
    return token_info

  
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
    session['refresh_token']= token_data['refresh_token']
    session['expires_at']= datetime.now().timestamp() + token_data['expires_in']
    
    return jsonify(token_data)

# @app.route('/get_recommendations')
# def getrecSongs():
#     if 'access_token' not in session: #check the access token 
#         return redirect('/login')
    
#     if datetime.now().timestamp() > session['expires_at']:
#         return redirect('/refresh-token') #automatically refresh it for them so we don't interrupt the user interface

#     headers = {
#         'Authorization': f"Bearer {session['access_token']}"
#     }

#     response = requests.get(API_BASE_URL + 'me/top/tracks', headers = headers)
#     tracks = response.json()

#     return tracks

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:  # check the refresh token
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        # make a request to get a fresh access token
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

    response = requests.post(TOKEN_URL, data=req_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp()
    + new_token_info['expires_in']

    return jsonify(new_token_info)


if __name__ == '__main__':
     app.run(host='0.0.0.0', debug=True)


