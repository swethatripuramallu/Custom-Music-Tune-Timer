import requests 
import urllib.parse

from flask import Flask, redirect, request, jsonify, session
from datetime import datetime, timedelta

# When you deploy this application make sure to copy over your own client id and secret.
# Saniya's Client ID, Client Secret
# CLIENT_ID = ''
# CLIENT_SECRET = ''
# REDIRECT_URL = ''

# Maggie's Client ID, Client Secret
# CLIENT_ID = ''
# CLIENT_SECRET = ''

# Swetha's Client ID, Client Secret 
# CLIENT_ID = '179f1cd011c44c25ab2e3658ac37b756'
# CLIENT_SECRET = '5460d929319845f19937d7441ad4ee51'
# REDIRECT_URL = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


def login():
    scope = 'user-read-private user-read-email'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URL,
        'show_dialog': True
        # Force the user to login everytime into application by setting show_dialog true 
        # to make debugging easier for local server purpose, can change at the end
    }
    #make a get request to user's data, also encoded the users params
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)



#Scenario for when the user fails to login successfully
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
            'redirect_uri': REDIRECT_URL,
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


    return  redirect('/playlists') #retrieves all the playlists


def get_playlists():
    if 'access_token' not in session: #check the access token 
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token') #automatically refresh it for them so we don't interrupt the user interface

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/playlists', headers = headers)
    playlists = response.json()

    return jsonify(playlists)

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

    return redirect('/playlist')