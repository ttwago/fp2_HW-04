from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_submit_data():
    data = {
        "pereval": {
            "beauty_title": "Тестовый перевал",
            "title": "Test Pereval",
            "other_titles": "Other Titles",
            "connect": "Test Connect",
            "coords": {
                "latitude": 123.456,
                "longitude": 789.012,
                "height": 1000
            },
            "level": {
                "winter": "Easy",
                "summer": "Moderate",
                "autumn": "Difficult",
                "spring": "Extreme"
            },
            "images": [
                {
                    "image_name": "image1.jpg",
                    "title": "Image 1"
                },
                {
                    "image_name": "image2.jpg",
                    "title": "Image 2"
                }
            ]
        }
    }

    response = client.post("/submitData", json=data)

    assert response.status_code == 200
    assert response.json()["status"] == 200
    assert response.json()["id"] is not None


def test_get_pereval_by_id():
    pereval_id = 1

    response = client.get(f"/submitData/{pereval_id}")

    assert response.status_code == 200
    assert "beauty_title" in response.json()
    assert "title" in response.json()
    assert "other_titles" in response.json()
    assert "connect" in response.json()
    assert "add_time" in response.json()
    assert "status" in response.json()
    assert "coords" in response.json()
    assert "level" in response.json()
    assert "images" in response.json()


def test_update_pereval():
    pereval_id = 1
    data = {
        "beauty_title": "Новое название",
        "title": "New Title",
        "other_titles": "New Other Titles",
        "connect": "New Connect",
        "coords": {
            "latitude": 111.222,
            "longitude": 333.444,
            "height": 2000
        },
        "level": {
            "winter": "Difficult",
            "summer": "Extreme",
            "autumn": "Easy",
            "spring": "Moderate"
        },
        "images": [
            {
                "image_name": "new_image1.jpg",
                "title": "New Image 1"
            },
            {
                "image_name": "new_image2.jpg",
                "title": "New Image 2"
            }
        ]
    }

    response = client.patch(f"/submitData/{pereval_id}", json=data)

    assert response.status_code == 200
    assert response.json()["state"] == 1
    assert response.json()["message"] == "Запись успешно обновлена"


def test_get_user_data():
    email = "test@example.com"

    response = client.get("/submitData", params={"user__email": email})

    assert response.status_code == 200
    assert isinstance(response.json(), list)
