import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_show_summary_valid_client(client):
    # Simulate a valid POST request with the correct email
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Add more assertions based on the expected behavior of your function
    # For example, you can check if certain content is present in the response HTML.

def test_show_summary_invalid_client(client):
    # Simulate a POST request with an invalid email
    response = client.post('/showSummary', data={'email': 'nonexistent@example.com'})

    # Assert that the response status code is 302 (redirect to index)
    assert response.status_code == 302

    # Assert that the response location header is set to redirect to the index
    assert response.headers['Location'] == 'http://localhost/'

    # Add more assertions if needed

# You can add more test cases to cover different scenarios

