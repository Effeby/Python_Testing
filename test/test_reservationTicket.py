import pytest
from flask import Flask, render_template, request, flash, get_flashed_messages
from server import app  # Assurez-vous que l'importation de l'application Flask est correcte

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_purchasePlaces(client):
    # Test pour le scénario où le club a des points suffisants
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '25'
    }

    response = client.post('/purchasePlaces', data=data)

    # Test pour le scénario où le club a des points insuffisants
    data['places'] = '1000'  # Assurez-vous que c'est un nombre supérieur aux points disponibles

    response = client.post('/purchasePlaces', data=data)
