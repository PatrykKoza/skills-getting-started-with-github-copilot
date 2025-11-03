import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@example.com"
    # Ensure user is not present
    client.delete(f"/activities/{activity}/participants/{email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Check participant added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
    # Remove participant
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    # Check participant removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

def test_signup_duplicate():
    activity = "Chess Club"
    email = "duplicate@example.com"
    client.delete(f"/activities/{activity}/participants/{email}")
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    client.delete(f"/activities/{activity}/participants/{email}")

def test_remove_nonexistent_participant():
    activity = "Chess Club"
    email = "notfound@example.com"
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404 or response.status_code == 200
