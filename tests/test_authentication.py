import pytest
from backend.userAuthentication import app

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