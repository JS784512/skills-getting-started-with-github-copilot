import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200  # Successful response
    # Since we're using TestClient, it follows redirects automatically

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    
    # Verify activity structure
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success():
    response = client.post(
        "/activities/Art Studio/signup",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up test@mergington.edu for Art Studio"

    # Verify the participant was actually added
    activities_response = client.get("/activities")
    assert "test@mergington.edu" in activities_response.json()["Art Studio"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post(
        "/activities/Drama Club/signup",
        params={"email": "actor@mergington.edu"}
    )
    
    # Try to signup again
    response = client.post(
        "/activities/Drama Club/signup",
        params={"email": "actor@mergington.edu"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_nonexistent_activity():
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "test@mergington.edu"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"