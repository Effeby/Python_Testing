import pytest
from flask import url_for
from datetime import datetime

from server import app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    # Mock data for testing
    test_clubs = [{'name': 'Simply Lift', 'points': '13'}]
    test_competitions = [{'name': 'Spring Festival', 'date': '2024-02-14 12:00:00'}]

    # Monkey patching the loadClubs and loadCompetitions functions
    app.loadClubs = lambda: test_clubs
    app.loadCompetitions = lambda: test_competitions

    # Valid test case
    response = client.get('/')
    assert response.status_code == 200
    assert b'Simply Lift' in response.data
    assert b'Spring Festival' in response.data

    # Invalid test case (no upcoming competitions)
    test_competitions[0]['date'] = '2022-01-01 12:00:00'
    response = client.get('/')
    assert response.status_code == 200
    assert b'Simply Lift' in response.data
    assert b'Fall Classic' not in response.data
