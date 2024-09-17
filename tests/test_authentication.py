import unittest
from unittest.mock import patch, MagicMock
from flask import session, Flask, redirect, request, jsonify, app
from datetime import datetime, timedelta
import requests 
import urllib.parse

# import unittest
# from app import app  # Adjust the import as necessary

class BasicTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()



# class TestSpotifyAuth(unittest.TestCase):
   
#     def setUp(self):
#         # Set up the Flask testing environment
#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'test'
#         self.app = app.test_client()

#     @patch('requests.post')
#     def test_login_redirect(self, mock_post):
#         # Test the /login endpoint to ensure it redirects correctly
#         response = self.app.get('/login')
#         self.assertEqual(response.status_code, 302)
#         self.assertIn('https://accounts.spotify.com/authorize', response.location)

#     @patch('requests.post')
#     def test_callback(self, mock_post):
#         # Mock the Spotify token response
#         mock_post.return_value = MagicMock(status_code=200)
#         mock_post.return_value.json.return_value = {
#             'access_token': 'mock_access_token',
#             'refresh_token': 'mock_refresh_token',
#             'expires_in': 3600
#         }

#         with self.app as client:
#             with client.session_transaction() as sess:
#                 sess['code'] = 'mock_code'

#             response = client.get('/callback?code=mock_code')
#             self.assertEqual(response.status_code, 302)
#             self.assertEqual(session['access_token'], 'mock_access_token')
#             self.assertEqual(session['refresh_token'], 'mock_refresh_token')
#             self.assertTrue('expires_at' in session)

#     @patch('requests.get')
#     def test_get_playlists(self, mock_get):
#         # Mock the Spotify playlists response
#         mock_get.return_value = MagicMock(status_code=200)
#         mock_get.return_value.json.return_value = {
#             'items': []
#         }

#         with self.app as client:
#             with client.session_transaction() as sess:
#                 sess['access_token'] = 'mock_access_token'
#                 sess['expires_at'] = datetime.now().timestamp() + 3600

#             response = client.get('/playlists')
#             self.assertEqual(response.status_code, 200)
#             self.assertIn('items', response.json)

# if __name__ == '__main__':
#     unittest.main()
