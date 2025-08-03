import pytest
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get('/')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'healthy'

def test_shorten_url(client):
    res = client.post('/api/shorten', json={"url": "https://example.com"})
    assert res.status_code == 200
    data = res.get_json()
    assert 'short_code' in data and len(data['short_code']) == 6
    assert 'short_url' in data

def test_invalid_url(client):
    res = client.post('/api/shorten', json={"url": "invalid-url"})
    assert res.status_code == 400
    assert "Invalid URL" in res.get_json()['error']

def test_redirect_and_clicks(client):
    # shorten url first
    res = client.post('/api/shorten', json={"url": "https://example.com"})
    short_code = res.get_json()['short_code']

    # redirect
    res_redirect = client.get(f'/{short_code}')
    assert res_redirect.status_code == 302
    assert res_redirect.location == "https://example.com"

    # redirect again to check clicks
    client.get(f'/{short_code}')

    # get stats, clicks should be 2
    res_stats = client.get(f'/api/stats/{short_code}')
    data = res_stats.get_json()
    assert data['clicks'] == 2

def test_stats_not_found(client):
    res = client.get('/api/stats/unknown')
    assert res.status_code == 404
