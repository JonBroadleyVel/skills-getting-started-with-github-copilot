from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_prevents_duplicate_registration():
    activity_name = "Chess Club"
    email = "duplicate-test@example.com"

    first = client.post(f"/activities/{activity_name}/signup?email={email}")
    second = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "remove-test@example.com"

    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]
