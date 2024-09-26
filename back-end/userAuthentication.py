import base64
import os
import requests 
import urllib.parse
from flask import Flask, redirect, request, jsonify, session
from datetime import datetime, timedelta
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

# Route to the flask app
@app.route('/')

# Welcome to app, with a hyperlink to login to spotify app
def index():
    return "Welcome to my Tune Timer <a href='/login'>Login with Spotify</a>" #planning on making this separate where it includes a react front end page for this 
 
#Redirect to Spotify Login Page, Need to declare scope/permissions
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


@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:  # check the refresh token
        return redirect('/login')

    if datetime.now().timestamp() . session['expires_at']:
        # make a request to get a fresh access token
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

    response = request.post(TOKEN_URL, data=req_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']
    session['expires_at'] = datetime.now().timestamp()
    + new_token_info['expires_in']

    return redirect('/playlist')


if __name__ == '__main__':
     app.run(host='0.0.0.0', debug=True)

