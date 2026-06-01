from urllib.parse import quote


def test_get_activities(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    url = f"/activities/{quote(activity_name, safe='')}/signup?email={quote(email, safe='')}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_duplicate_signup_returns_bad_request(client):
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"
    url = f"/activities/{quote(activity_name, safe='')}/signup?email={quote(email, safe='')}"

    # Act
    first = client.post(url)
    second = client.post(url)

    # Assert
    assert first.status_code == 200
    assert second.status_code == 400
    assert "already signed up" in second.json()["detail"]


def test_unregister_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{quote(activity_name, safe='')}/participants?email={quote(email, safe='')}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
