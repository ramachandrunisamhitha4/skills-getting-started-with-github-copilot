"""
Tests for the High School Management System API.
"""

import copy
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

INITIAL_ACTIVITIES = copy.deepcopy(activities)


def setup_function(function):
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def teardown_function(function):
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def test_get_activities_returns_initial_data():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "newuser@mergington.edu"})
    assert response.status_code == 200
    assert "newuser@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400():
    client.post("/activities/Chess Club/signup", params={"email": "newuser@mergington.edu"})
    response = client.post("/activities/Chess Club/signup", params={"email": "newuser@mergington.edu"})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_remove_participant_success():
    response = client.delete("/activities/Chess Club/participants", params={"email": "michael@mergington.edu"})
    assert response.status_code == 200
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_participant_not_found():
    response = client.delete("/activities/Chess Club/participants", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_activity_not_found_for_signup():
    response = client.post("/activities/NoActivity/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404


def test_activity_not_found_for_remove():
    response = client.delete("/activities/NoActivity/participants", params={"email": "test@mergington.edu"})
    assert response.status_code == 404