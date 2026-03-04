import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint(client):
    """Test the main hello endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Docker Security Lab: Application Running Safely!" in response.data

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_security_headers(client):
    """Verify that security headers are present in the response."""
    response = client.get('/')
    assert response.headers['X-Frame-Options'] == 'DENY'
    assert response.headers['X-Content-Type-Options'] == 'nosniff'
    assert response.headers['X-XSS-Protection'] == '1; mode=block'
    assert "default-src 'self'" in response.headers['Content-Security-Policy']
