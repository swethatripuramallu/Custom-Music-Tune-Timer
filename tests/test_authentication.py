import pytest
from backend.userAuthentication import app
from datetime import datetime, timedelta

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to my Tune Timer" in response.data

def test_login_redirect(client):
    """Test the login route redirection to Spotify."""
    response = client.get('/login')
    assert response.status_code == 302  # 302 is for redirect
    assert "https://accounts.spotify.com/authorize" in response.location

# def test_callback_error(client):
#     """Test the callback route when there's an error in the request args."""
#     response = client.get('/callback', query_string={"error": "access_denied"})
#     assert response.status_code == 200
#     assert b'"error": "access_denied"' in response.data

# def test_callback_success(client, monkeypatch):
#     """Test the callback route with successful authorization."""
#     def mock_post(url, data):
#         return MockResponse({
#             "access_token": "mock_access_token",
#             "refresh_token": "mock_refresh_token",
#             "expires_in": 3600
#         })

#     monkeypatch.setattr("requests.post", mock_post)

#     with client.session_transaction() as session:
#         session['CLIENT_ID'] = 'test_client_id'
#         session['CLIENT_SECRET'] = 'test_client_secret'
#         session['REDIRECT_URL'] = 'http://localhost/callback'

#     response = client.get('/callback', query_string={"code": "valid_code"})
#     assert response.status_code == 302  # Expect a redirect to '/playlists'
#     assert response.location.endswith('/playlists')

# def test_get_playlists_no_token(client):
#     """Test the playlists route when no access token is present."""
#     response = client.get('/playlists')
#     assert response.status_code == 302  # Redirect to login
#     assert "/login" in response.location

# def test_get_playlists_with_token(client, monkeypatch):
#     """Test the playlists route with a valid access token."""
#     def mock_get(url, headers):
#         return MockResponse({
#             "items": [{"name": "Playlist 1"}, {"name": "Playlist 2"}]
#         })

#     monkeypatch.setattr("requests.get", mock_get)

#     with client.session_transaction() as session:
#         session['access_token'] = 'mock_access_token'
#         session['expires_at'] = datetime.now().timestamp() + 3600

#     response = client.get('/playlists')
#     assert response.status_code == 200
#     assert b"Playlist 1" in response.data
#     assert b"Playlist 2" in response.data

# # Helper class for mocking responses
# class MockResponse:
#     def __init__(self, json_data, status_code=200):
#         self.json_data = json_data
#         self.status_code = status_code

#     def json(self):
#         return self.json_data