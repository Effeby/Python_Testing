import json
from datetime import datetime, timedelta
from server import app

def test_competitions_date_filter():
    with app.test_request_context():
        today = datetime.now()
        competitions = [
            {"name": "Spring Festival", "date": "2025-03-27 10:00:00", "numberOfPlaces": "5"},
            {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
            {"name": "LDC", "date": "2024-10-22 13:30:00", "numberOfPlaces": "32"},
        ]

        app.config['competitions'] = competitions  # Set the app's competitions

        client = app.test_client()
        response = client.get('/')

        print(response.data.decode())  # Ajout d'une impression pour débogage

        assert response.status_code == 200
        assert b"Spring Festival" in response.data
        assert b"Fall Classic" not in response.data
        assert b"LDC" in response.data
