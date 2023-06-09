from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get('message') == 'Hello World!'
    assert res.status_code == 200


def test_create_user():
    res = client.post(
        "/users/", json={"email": "test@gmail.com", "password": "test123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201
