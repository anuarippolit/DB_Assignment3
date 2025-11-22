import pytest
from app.models.enums import CaregivingType, Gender
from io import BytesIO

def test_create_caregiver(client):
    user_response = client.post(
        "/users/",
        data={
            "email": "caregiver@example.com",
            "given_name": "Caregiver",
            "surname": "Test",
            "city": "Astana",
            "phone_number": "+77075555555",
            "password": "password123"
        }
    )
    
    user_id = user_response.json()["user_id"]
    
    photo_file = BytesIO(b"fake photo content")
    response = client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": user_id,
            "gender": Gender.MALE.value,
            "caregiving_type": CaregivingType.ELDERLY_CARE.value,
            "hourly_rate": 1500
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    assert response.status_code == 201
    data = response.json()

    assert data["caregiver_user_id"] == user_id
    assert data["caregiving_type"] == CaregivingType.ELDERLY_CARE.value
    assert data["hourly_rate"] == 1500

def test_get_caregiver(client):
    user_response = client.post(
        "/users/",
        data={
            "email": "caregiver2@example.com",
            "given_name": "Caregiver2",
            "surname": "Test2",
            "city": "Almaty",
            "phone_number": "+77076666666",
            "password": "password123"
        }
    )
    user_id = user_response.json()["user_id"]
    
    photo_file = BytesIO(b"fake photo content")
    client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": user_id,
            "gender": Gender.FEMALE.value,
            "caregiving_type": CaregivingType.BABYSITTER.value,
            "hourly_rate": 1200
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    
    response = client.get(f"/caregivers/{user_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["caregiver_user_id"] == user_id
    assert data["caregiving_type"] == CaregivingType.BABYSITTER.value

def test_update_caregiver(client):
    user_response = client.post(
        "/users/",
        data={
            "email": "caregiver3@example.com",
            "given_name": "Caregiver3",
            "surname": "Test3",
            "city": "Astana",
            "phone_number": "+77077777777",
            "password": "password123"
        }
    )
    user_id = user_response.json()["user_id"]
    
    photo_file = BytesIO(b"fake photo content")
    client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": user_id,
            "gender": Gender.MALE.value,
            "caregiving_type": CaregivingType.ELDERLY_CARE.value,
            "hourly_rate": 1500
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    
    response = client.put(
        f"/caregivers/{user_id}?hourly_rate=2000"
    )
    assert response.status_code == 200
    data = response.json()

    assert data["hourly_rate"] == 2000

def test_delete_caregiver(client):
    user_response = client.post(
        "/users/",
        data={
            "email": "caregiver4@example.com",
            "given_name": "Caregiver4",
            "surname": "Test4",
            "city": "Astana",
            "phone_number": "+77078888888",
            "password": "password123"
        }
    )

    user_id = user_response.json()["user_id"]
    
    photo_file = BytesIO(b"fake photo content")
    client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": user_id,
            "gender": Gender.FEMALE.value,
            "caregiving_type": CaregivingType.PLAYMATE_FOR_CHILDREN.value,
            "hourly_rate": 1000
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    
    response = client.delete(f"/caregivers/{user_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/caregivers/{user_id}")
    assert get_response.status_code == 404

