import pytest
from flask import url_for

from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_logout(client):
    # Ensure the /logout route redirects to the /index route
    response = client.get('/logout')
    print(f"Response Headers: {response.headers}")
    assert response.status_code == 302  # HTTP status code for redirect
    assert response.headers['Location'] in ('/', '/index')


    # Alternatively, you can use Flask's url_for to get the URL dynamically
    response = client.get(url_for('logout'))
    print(f"Response Headers: {response.headers}")
    assert response.status_code == 302
    assert response.headers['Location'] in ('/', '/index')
