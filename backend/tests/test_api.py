from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['service'] == 'smart-tourist-safety-and-travel-assistant-api'


def test_demo_login_for_tourist() -> None:
    response = client.post('/auth/login', json={'email': 'tourist@demo.com', 'password': 'demo123'})
    assert response.status_code == 200
    body = response.json()
    assert body['role'] == 'tourist'
    assert body['access_token'].startswith('demo-token-')


def test_trip_creation_and_listing() -> None:
    create_response = client.post(
        '/trips',
        json={
            'user_name': 'Alex Tourist',
            'city': 'Jaipur',
            'start_date': '2026-03-21',
            'end_date': '2026-03-23',
            'travelers': 2,
            'interests': ['heritage', 'food'],
        },
    )
    assert create_response.status_code == 200
    trip = create_response.json()
    assert trip['city'] == 'Jaipur'
    assert trip['status'] == 'planned'

    list_response = client.get('/trips')
    assert list_response.status_code == 200
    assert any(item['id'] == trip['id'] for item in list_response.json())


def test_safety_score_detects_risk_zone() -> None:
    response = client.get('/safety/score', params={'lat': 26.9162, 'lng': 75.8208})
    assert response.status_code == 200
    body = response.json()
    assert body['score'] < 75
    assert body['nearby_zone']
    assert body['level'] in {'MEDIUM', 'HIGH'}


def test_sos_and_incident_flow_show_up_in_admin_views() -> None:
    sos_response = client.post(
        '/sos/trigger',
        json={
            'traveler_name': 'Alex Tourist',
            'city': 'Jaipur',
            'latitude': 26.9124,
            'longitude': 75.7873,
            'message': 'Need urgent assistance near MI Road',
            'trigger_method': 'button',
        },
    )
    assert sos_response.status_code == 200
    sos_body = sos_response.json()
    assert sos_body['status'] == 'active'

    incident_response = client.post(
        '/incidents',
        json={
            'traveler_name': 'Alex Tourist',
            'category': 'theft',
            'city': 'Jaipur',
            'description': 'Phone snatching attempt near the market',
            'latitude': 26.9162,
            'longitude': 75.8208,
            'severity': 4,
        },
    )
    assert incident_response.status_code == 200

    summary_response = client.get('/admin/dashboard/summary')
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary['active_sos'] >= 1
    assert summary['open_incidents'] >= 1

    admin_sos = client.get('/admin/sos')
    admin_incidents = client.get('/admin/incidents')
    assert admin_sos.status_code == 200
    assert admin_incidents.status_code == 200
    assert any(item['id'] == sos_body['id'] for item in admin_sos.json())
    assert any(item['category'] == 'theft' for item in admin_incidents.json())


def test_frontend_pages_render() -> None:
    tourist_response = client.get('/')
    admin_response = client.get('/admin')
    assert tourist_response.status_code == 200
    assert admin_response.status_code == 200
    assert 'Smart Tourist Safety & Travel Assistant' in tourist_response.text
    assert 'Tourist Safety Admin Dashboard' in admin_response.text
