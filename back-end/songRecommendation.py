import requests 
import urllib.parse

from flask import Flask, redirect, request, jsonify, session
from datetime import datetime, timedelta

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