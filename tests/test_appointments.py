import pytest
from datetime import date, time
from app.models.enums import AppointmentStatus, Gender, CaregivingType
from io import BytesIO

def test_create_appointment(client):
    caregiver_user_response = client.post(
        "/users/",
        data={
            "email": "caregiver_appt@example.com",
            "given_name": "Caregiver",
            "surname": "Appt",
            "city": "Astana",
            "phone_number": "+77071111111",
            "password": "password123"
        }
    )
    caregiver_user_id = caregiver_user_response.json()["user_id"]
    
    photo_file = BytesIO(b"fake photo content")
    client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "gender": Gender.MALE.value,
            "caregiving_type": CaregivingType.ELDERLY_CARE.value,
            "hourly_rate": 1500
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    
    member_user_response = client.post(
        "/users/",
        data={
            "email": "member_appt@example.com",
            "given_name": "Member",
            "surname": "Appt",
            "city": "Almaty",
            "phone_number": "+77072222222",
            "password": "password123"
        }
    )
    member_user_id = member_user_response.json()["user_id"]
    
    client.post(
        "/members/",
        data={
            "member_user_id": member_user_id
        }
    )
    
    future_date = date.today().replace(day=date.today().day + 1) if date.today().day < 28 else date.today().replace(month=date.today().month + 1, day=1)
    response = client.post(
        "/appointments/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "member_user_id": member_user_id,
            "appointment_date": future_date.isoformat(),
            "appointment_time": "10:00:00",
            "work_hours": 4,
            "status": AppointmentStatus.PENDING.value
        }
    )
    assert response.status_code == 201
    data = response.json()

    assert data["caregiver_user_id"] == caregiver_user_id
    assert data["member_user_id"] == member_user_id
    assert data["status"] == AppointmentStatus.PENDING.value

    assert "appointment_id" in data

def test_get_appointment(client):
    caregiver_user_response = client.post(
        "/users/",
        data={
            "email": "caregiver_appt2@example.com",
            "given_name": "Caregiver2",
            "surname": "Appt2",
            "city": "Astana",
            "phone_number": "+77073333333",
            "password": "password123"
        }
    )
    caregiver_user_id = caregiver_user_response.json()["user_id"]
    
    photo_file = BytesIO(b"fake photo content")
    client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "gender": Gender.FEMALE.value,
            "caregiving_type": CaregivingType.BABYSITTER.value,
            "hourly_rate": 1200
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    
    member_user_response = client.post(
        "/users/",
        data={
            "email": "member_appt2@example.com",
            "given_name": "Member2",
            "surname": "Appt2",
            "city": "Almaty",
            "phone_number": "+77074444444",
            "password": "password123"
        }
    )
    member_user_id = member_user_response.json()["user_id"]
    
    client.post(
        "/members/",
        data={
            "member_user_id": member_user_id
        }
    )
    
    future_date = date.today().replace(day=date.today().day + 1) if date.today().day < 28 else date.today().replace(month=date.today().month + 1, day=1)
    create_response = client.post(
        "/appointments/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "member_user_id": member_user_id,
            "appointment_date": future_date.isoformat(),
            "appointment_time": "14:00:00",
            "work_hours": 6,
            "status": AppointmentStatus.ACCEPTED.value
        }
    )
    appointment_id = create_response.json()["appointment_id"]
    
    response = client.get(f"/appointments/{appointment_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["appointment_id"] == appointment_id
    assert data["status"] == AppointmentStatus.ACCEPTED.value

def test_get_appointments(client):
    caregiver_user_response = client.post(
        "/users/",
        data={
            "email": "caregiver_appt3@example.com",
            "given_name": "Caregiver3",
            "surname": "Appt3",
            "city": "Astana",
            "phone_number": "+77075555555",
            "password": "password123"
        }
    )
    caregiver_user_id = caregiver_user_response.json()["user_id"]
    
    photo_file = BytesIO(b"fake photo content")
    client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "gender": Gender.MALE.value,
            "caregiving_type": CaregivingType.ELDERLY_CARE.value,
            "hourly_rate": 1500
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    
    member_user_response = client.post(
        "/users/",
        data={
            "email": "member_appt3@example.com",
            "given_name": "Member3",
            "surname": "Appt3",
            "city": "Almaty",
            "phone_number": "+77076666666",
            "password": "password123"
        }
    )
    member_user_id = member_user_response.json()["user_id"]
    
    client.post(
        "/members/",
        data={
            "member_user_id": member_user_id
        }
    )
    
    future_date = date.today().replace(day=date.today().day + 1) if date.today().day < 28 else date.today().replace(month=date.today().month + 1, day=1)
    client.post(
        "/appointments/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "member_user_id": member_user_id,
            "appointment_date": future_date.isoformat(),
            "appointment_time": "09:00:00",
            "work_hours": 3,
            "status": AppointmentStatus.PENDING.value
        }
    )
    

    response = client.get("/appointments/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    assert len(data) > 0


def test_update_appointment(client):
    caregiver_user_response = client.post(
        "/users/",
        data={
            "email": "caregiver_appt4@example.com",
            "given_name": "Caregiver4",
            "surname": "Appt4",
            "city": "Astana",
            "phone_number": "+77077777777",
            "password": "password123"
        }
    )
    caregiver_user_id = caregiver_user_response.json()["user_id"]
    
    photo_file = BytesIO(b"content")
    client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "gender": Gender.FEMALE.value,
            "caregiving_type": CaregivingType.BABYSITTER.value,
            "hourly_rate": 1200
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    
    member_user_response = client.post(
        "/users/",
        data={
            "email": "member_appt4@example.com",
            "given_name": "Member4",
            "surname": "Appt4",
            "city": "Almaty",
            "phone_number": "+77078888888",
            "password": "password123"
        }
    )
    member_user_id = member_user_response.json()["user_id"]
    
    client.post(
        "/members/",
        data={
            "member_user_id": member_user_id
        }
    )
    
    future_date = date.today().replace(day=date.today().day + 1) if date.today().day < 28 else date.today().replace(month=date.today().month + 1, day=1)
    create_response = client.post(
        "/appointments/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "member_user_id": member_user_id,
            "appointment_date": future_date.isoformat(),
            "appointment_time": "11:00:00",
            "work_hours": 5,
            "status": AppointmentStatus.PENDING.value
        }
    )
    appointment_id = create_response.json()["appointment_id"]
    
    response = client.put(
        f"/appointments/{appointment_id}?status={AppointmentStatus.ACCEPTED.value}&work_hours=6"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == AppointmentStatus.ACCEPTED.value
    assert data["work_hours"] == 6

def test_delete_appointment(client):
    caregiver_user_response = client.post(
        "/users/",
        data={
            "email": "caregiver_appt5@example.com",
            "given_name": "Caregiver5",
            "surname": "Appt5",
            "city": "Astana",
            "phone_number": "+77079999999",
            "password": "password123"
        }
    )
    caregiver_user_id = caregiver_user_response.json()["user_id"]
    
    photo_file = BytesIO(b"fake photo content")
    client.post(
        "/caregivers/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "gender": Gender.MALE.value,
            "caregiving_type": CaregivingType.ELDERLY_CARE.value,
            "hourly_rate": 1500
        },
        files={"photo": ("photo.jpg", photo_file, "image/jpeg")}
    )
    
    member_user_response = client.post(
        "/users/",
        data={
            "email": "member_appt5@example.com",
            "given_name": "Member5",
            "surname": "Appt5",
            "city": "Almaty",
            "phone_number": "+77071010101",
            "password": "password123"
        }
    )
    member_user_id = member_user_response.json()["user_id"]
    
    client.post(
        "/members/",
        data={
            "member_user_id": member_user_id
        }
    )
    
    future_date = date.today().replace(day=date.today().day + 1) if date.today().day < 28 else date.today().replace(month=date.today().month + 1, day=1)
    create_response = client.post(
        "/appointments/",
        data={
            "caregiver_user_id": caregiver_user_id,
            "member_user_id": member_user_id,
            "appointment_date": future_date.isoformat(),
            "appointment_time": "15:00:00",
            "work_hours": 4,
            "status": AppointmentStatus.DECLINED.value
        }
    )
    appointment_id = create_response.json()["appointment_id"]
    
    response = client.delete(f"/appointments/{appointment_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/appointments/{appointment_id}")
    assert get_response.status_code == 404

