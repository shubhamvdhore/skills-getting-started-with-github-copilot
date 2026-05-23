from urllib.parse import quote

from src.app import activities


def test_root_redirects_to_static_index(client):
    # Arrange / Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange / Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "test_student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={quote(email, safe='')}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "duplicate_student@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={quote(email, safe='')}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={quote(email, safe='')}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = activities["Chess Club"]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={quote(email, safe='')}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    email = "missing_student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={quote(email, safe='')}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_remove_from_missing_activity_returns_404(client):
    # Arrange
    activity_name = quote("Nonexistent Club", safe="")
    email = "missing_student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={quote(email, safe='')}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
