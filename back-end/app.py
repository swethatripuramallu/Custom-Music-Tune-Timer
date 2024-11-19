import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import time
from flask_cors import CORS
from cachelib.file import FileSystemCache

from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

from base64 import b64encode
import io
from PIL import Image

load_dotenv()

app = Flask(__name__)

CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')

cache = FileSystemCache('/tmp/flask_cache')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


def get_spotify_client():
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=('user-library-read '
               'user-read-recently-played '
               'playlist-modify-public '
               'user-top-read '
               'playlist-read-collaborative '
               'user-read-playback-state '
               'ugc-image-upload '
               'user-modify-playback-state'),
        cache_path='.cache'
    ))

    return sp


def parse_songs(recommended):

    tracks = []

    recommendedTracks = recommended.get('tracks', [])

    for item in recommendedTracks:
        track_name = item['name']
        artists = item.get('artists', [])
        artist_names = ", ".join([artist.get('name', 'Unknown Artist')
                                  for artist in artists])
        duration = item['duration_ms']
        track_id = item.get('id', "Unknown ID")

        song_info = {
            'track_name': track_name,
            'artist_name': artist_names,
            'duration': duration,
            'track_id': track_id
        }

        tracks.append(song_info)

    return tracks


def filterSongsByDuration(tracks: list, duration: float):
    # sort tracks by duration in descending order
    # sorted_tracks = sorted(tracks, key=lambda x: x['duration'], reverse=True)

    selected_tracks = []
    current_duration = 0

    for track in tracks:
        if current_duration + track['duration'] <= duration:
            selected_tracks.append(track)
            current_duration += track['duration']

        if current_duration >= duration:
            break

    return selected_tracks


# Function to encode cover image to base64
def encode_image_to_base64(image_path):
    with Image.open(image_path) as img:
        img = img.resize((300, 300))  # Spotify requires 300x300 px images
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        return b64encode(buffered.getvalue()).decode('utf-8')


# Function to fetch Spotify data based on user input
def get_spotify_data(length, happy, sad, dance, productive):
    sp = get_spotify_client()

    # Modify recommendations based on moods or user input (happy, sad, etc.)
    min_danceability = 0.0
    target_danceability = 0.5
    min_tempo = 0.0
    target_tempo = 120.0
    max_speechiness = 1.0
    max_loudness = 1.0
    min_valence = 0.0
    max_valence = 1.0
    target_valence = 0.5
    min_energy = 0.0
    target_energy = 0.5
    max_energy = 1.0
    min_acousticness = 0.0
    min_instrumentalness = 0.0
    max_tempo = 200.0
    target_tempo = 120.0
    seed_genres = []
    if happy:
        min_tempo = 100.0
        target_tempo = 140.0
        min_valence = 0.5
        target_valence = 0.8
        min_energy = 0.6
        target_energy = 0.8
        seed_genres.append('happy')
    if sad:
        min_acousticness = 0.4
        max_tempo = 80.0
        target_tempo = 60.0
        max_valence = 0.5
        target_valence = 0.2
        max_energy = 0.4
        seed_genres.append('sad')
    if dance:
        min_danceability = 0.6
        target_danceability = 0.8
        min_energy = 0.7
        target_energy = 0.85
        min_tempo = 110.0
        target_tempo = 130.0
        seed_genres.append('dance')
    if productive:
        max_speechiness = 0.4
        max_loudness = 0.4
        target_tempo = 120.0
        target_energy = 0.4
        min_instrumentalness = 0.7
        seed_genres.append('study')

    # Seeds based on user tracks and user artists
    top_tracks = sp.current_user_top_tracks(limit=1)
    seed_tracks = [track['id'] for track in top_tracks['items']]

    top_artists = sp.current_user_top_artists(limit=3, time_range='long_term')
    seed_artists = [artist['id'] for artist in top_artists['items']]

    # Fetch recommended songs based on mood
    recs = sp.recommendations(seed_tracks=seed_tracks,
                              seed_artists=seed_artists,
                              seed_genres=seed_genres,
                              min_danceability=min_danceability,
                              target_danceability=target_danceability,
                              max_speechiness=max_speechiness,
                              max_loudness=max_loudness,
                              min_tempo=min_tempo,
                              target_tempo=target_tempo,
                              max_tempo=max_tempo,
                              min_acousticness=min_acousticness,
                              min_instrumentalness=min_instrumentalness,
                              min_energy=min_energy,
                              target_energy=target_energy,
                              max_energy=max_energy,
                              min_valence=min_valence,
                              max_valence=max_valence,
                              target_valence=target_valence,
                              limit=100)

    tracks = parse_songs(recs)
    filtered_songs = filterSongsByDuration(tracks, length)

    # Create a new playlist
    user_id = sp.current_user()['id']
    name = "Tune Timer Playlist"
    description = "A playlist created based on your selected mood and time."
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True,
                                       description=description)
    # Get the track URIs for the filtered songs
    track_uris = [f"spotify:track:{track['track_id']}" for track
                  in filtered_songs]

    # Add tracks to the new playlist
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

    # Return the playlist information along with track data
    response_data = {
        'playlist_id': playlist['id'],
        'playlist_url': playlist['external_urls']['spotify'],
        'tracks': filtered_songs
    }

    # Set the custom playlist cover
    cover_image_path = '../assets/images/cover.png'
    base64_image = encode_image_to_base64(cover_image_path)
    sp.playlist_upload_cover_image(playlist_id=playlist['id'],
                                   image_b64=base64_image)

    return response_data


@app.route('/callback')
def callback():
    return "Authentication Sucessful!"


# Flask route to handle playlist creation
@app.route('/create-playlist', methods={'POST'})
def create_playlist():
    data = request.get_json()  # Parse incoming JSON request body
    print('Received data:', data)

    length = int(data.get('length')) * 60000
    happy = data.get('happy')
    sad = data.get('sad')
    dance = data.get('dance')
    productive = data.get('productive')

    # Get Spotify data based on mood
    spotify_data = get_spotify_data(length, happy, sad, dance, productive)

    tracks = spotify_data['tracks']

    # print("Spotify Data:", spotify_data)
    for track in tracks:
        track_name = track['track_name']
        track_artist = track['artist_name']
        print(f"{track_name} by {track_artist}")

    return jsonify(spotify_data)


@app.route('/play')
def play_playlist():
    sp = get_spotify_client()

    # Get device ID
    for device in sp.devices()['devices']:
        if device['is_active']:
            device_id = device['id']
    print(device_id)

    # Get user ID
    user_id = sp.current_user()['id']
    print(user_id)

    # Get TUNE TIMER PLAYLIST ID
    for playlist in sp.user_playlists(user=user_id)['items']:
        if playlist['name'] == 'Tune Timer Playlist':
            playlist_id = playlist['id']
            break
    print(playlist_id)

    sp.start_playback(device_id=device_id,
                      context_uri="spotify:playlist:" + playlist_id,
                      offset={"position": 0})
    # return "Playing Playlist"
    playlist_length = 0.0
    for track in sp.playlist_items(playlist_id=playlist_id)['items']:
        playlist_length += track['track']['duration_ms']

    print("playlist length", playlist_length)
    return jsonify(playlist_length)


@app.route('/resume')
def resume_playlist():
    sp = get_spotify_client()

    # Get device ID
    device_id = None
    for device in sp.devices()['devices']:
        if device['is_active']:
            device_id = device['id']

    sp.start_playback(device_id=device_id)

    return jsonify("Resuming Playlist")


@app.route('/pause')
def pause_playlist():
    sp = get_spotify_client()

    # Get device ID
    device_id = None
    for device in sp.devices()['devices']:
        if device['is_active']:
            device_id = device['id']

    sp.pause_playback(device_id=device_id)

    return jsonify("Pausing Playlist")


@app.route('/alarm')
def alarm():
    sp = get_spotify_client()

    # Get device ID
    device_id = None
    for device in sp.devices()['devices']:
        if device['is_active']:
            device_id = device['id']

    track_uri = "2quaZxFrp6N4lNrajGLnAW"

    sp.start_playback(device_id=device_id,
                      context_uri="spotify:album:" + track_uri,
                      offset={"position": 78})

    time.sleep(5)
    pause_playlist()

    return jsonify("Playing Alarm")


@app.route('/delete')
def delete_playlist():
    sp = get_spotify_client()

    # Get user ID
    user_id = sp.current_user()['id']

    # Get playlist ID
    for playlist in sp.user_playlists(user=user_id)['items']:
        if playlist['name'] == 'Tune Timer Playlist':
            playlist_id = playlist['id']
            break

    # Delete (unfollow) playlist
    sp.current_user_unfollow_playlist(playlist_id=playlist_id)

    return jsonify("Playlist Deleted")


@app.route('/most-recent-playlist')
def most_recent_playlist():
    sp = get_spotify_client()

    # Get user ID
    user_id = sp.current_user()['id']
    playlist_info = None

    # Get playlist ID and name
    for playlist in sp.user_playlists(user=user_id)['items']:
        if playlist['name'] == 'Tune Timer Playlist':
            playlist_info = {
                "playlist_id": playlist['id'],
                "name": playlist['name']
            }
            break
    
    if playlist_info:
        playlist = sp.playlist(playlist_info['playlist_info'])
        # Extract track added dates
        added_at_dates = [
            item['added_at'] for item in playlist['tracks']['items'] if item['added_at']
        ]

        # Find the earliest added_at date
        if added_at_dates:
            earliest_date = min(added_at_dates)
        return jsonify({
            "playlist_modified": earliest_date,
            "name": playlist_info['name'],
            "message": "Successfully retrieved playlist information."
        })
    else:
        return jsonify({
            "error": "Playlist not found."
        }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'), debug=True)
