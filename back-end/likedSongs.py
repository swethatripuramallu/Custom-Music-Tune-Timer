# from flask import Flask, app, session, redirect, jsonify
# import os, time, logging, requests

# app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY')

# CLIENT_ID = os.getenv('CLIENT_ID')
# CLIENT_SECRET = os.getenv('CLIENT_SECRET')
# REDIRECT_URI = os.getenv('REDIRECT_URI')

# AUTH_URL = 'https://accounts.spotify.com/authorize'
# TOKEN_URL = 'https://accounts.spotify.com/api/token'
# API_BASE_URL = 'https://api.spotify.com/v1/'

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# @app.route('/liked-songs')
# def liked_songs():
#     access_token = session.get('access_token')
#     if not access_token:
#         logging.error("Access token not found in session.")
#         return redirect('/login')

#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
    
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
    
# if __name__ == '__main__':
#     app.run(port='5001', debug=True)