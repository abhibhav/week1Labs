import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_list_activities():
    # Arrange: (No setup needed for in-memory activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v for v in data.values())

def test_signup_and_prevent_duplicate():
    # Arrange
    activity_name = next(iter(client.get("/activities").json().keys()))
    email = "student1@mergington.edu"

    # Act
    response1 = client.post(f"/activities/{activity_name}/signup?email={email}")
    response2 = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response1.status_code == 200
    assert response2.status_code != 200  # Should not allow duplicate registration

    # Check participant is only once in the list
    activities = client.get("/activities").json()
    participants = activities[activity_name]["participants"]
    assert participants.count(email) == 1
