import json
import pytest
from server import app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_book(client):
    # Mock data for testing
    test_clubs = [{'name': 'Simply Lift', 'points': '13'}]
    test_competitions = [{'name': 'Spring Festival', 'numberOfPlaces': '5'}]

    # Monkey patching the loadClubs and loadCompetitions functions
    app.loadClubs = lambda: test_clubs
    app.loadCompetitions = lambda: test_competitions

    # Debugging: Print the data returned by loadClubs and loadCompetitions
    print("Test Clubs:", app.loadClubs())
    print("Test Competitions:", app.loadCompetitions())

    # Valid test case
    response = client.get('/book/Spring%20Festival/Simply%20Lift')
    assert response.status_code == 200
    assert b'Simply Lift' in response.data
    assert b'Spring Festival' in response.data

    # Invalid test case (club not found)
    response = client.get('/book/NonexistentCompetition/Simply%20Lift')
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data

    # Invalid test case (competition not found)
    response = client.get('/book/Spring%20Festival/NonexistentClub')
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data

    # Invalid test case (both club and competition not found)
    response = client.get('/book/NonexistentCompetition/NonexistentClub')
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data
