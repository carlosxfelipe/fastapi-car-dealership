from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_all_cars():
    response = client.get("/cars")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_car_by_id():
    cars = client.get("/cars").json()
    car_id = cars[0]["id"]
    response = client.get(f"/cars/{car_id}")
    assert response.status_code == 200
    assert response.json()["id"] == car_id


def test_get_car_not_found():
    response = client.get("/cars/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_create_car():
    response = client.post("/cars", json={"brand": "Ford", "model": "Mustang"})
    assert response.status_code == 201
    data = response.json()
    assert data["brand"] == "Ford"
    assert data["model"] == "Mustang"
    assert "id" in data


def test_create_car_invalid():
    response = client.post("/cars", json={"brand": "F", "model": "M"})
    assert response.status_code == 422


def test_create_car_extra_field_forbidden():
    response = client.post(
        "/cars", json={"brand": "Ford", "model": "Mustang", "year": 2024}
    )
    assert response.status_code == 422


def test_update_car():
    cars = client.get("/cars").json()
    car_id = cars[0]["id"]
    response = client.patch(f"/cars/{car_id}", json={"brand": "Updated"})
    assert response.status_code == 200
    assert response.json()["brand"] == "Updated"


def test_update_car_not_found():
    response = client.patch(
        "/cars/12345678-1234-1234-1234-123456789abc", json={"brand": "XX"}
    )
    assert response.status_code == 404


def test_delete_car():
    cars = client.get("/cars").json()
    car_id = cars[-1]["id"]
    response = client.delete(f"/cars/{car_id}")
    assert response.status_code == 200
    assert str(car_id) in response.json()["message"]


def test_delete_car_not_found():
    response = client.delete("/cars/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
