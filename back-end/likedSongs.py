# from flask import Blueprint, session, redirect, jsonify
# import requests
# import os
# import logging
# import time

# liked_songs_bp = Blueprint('liked_songs', __name__)

# API_BASE_URL = 'https://api.spotify.com/v1/'

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# @liked_songs_bp.route('/liked-songs')
# def liked_songs():
#     access_token = session.get('access_token')
#     if not access_token:
#         logging.error("Access token not found in session.")
#         return redirect('/login')

#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
    
#     limit = 50
#     start_time = time.time()
#     try:
#         response = requests.get(f'{API_BASE_URL}me/tracks?limit={limit}', headers=headers, timeout=10)
#     except requests.exceptions.Timeout:
#         logging.error("Request to Spotify API timed out.")
#         return jsonify({'error': 'Request to Spotify API timed out'}), 504

#     end_time = time.time()
#     logging.debug(f"Request URL: {response.url}")
#     logging.debug(f"Response Status Code: {response.status_code}")
#     logging.debug(f"Response Content: {response.content}")
#     logging.debug(f"Time taken for request: {end_time - start_time} seconds")

#     if response.status_code != 200:
#         logging.error(f"Failed to fetch liked songs: {response.content}")
#         return jsonify({'error': 'Failed to fetch liked songs'}), response.status_code

#     data = response.json()
#     liked_songs = []

#     for item in data['items']:
#         track = item['track']
#         song_info = {
#             'name': track['name'],
#             'artist': track['artists'][0]['name'],
#             'album': track['album']['name'],
#             'added_at': item['added_at']
#         }
#         liked_songs.append(song_info)

#     if len(liked_songs) < 50:
#         return jsonify({'message': 'User has fewer than 50 liked songs', 'liked_songs': liked_songs})
#     else:
#         return jsonify(liked_songs)