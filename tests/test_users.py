def test_create_user(client):
    response = client.post(
        "/users/",
        data={
            "email": "test@example.com",
            "given_name": "Test",
            "surname": "User",
            "city": "Astana",
            "phone_number": "+77071234567",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["given_name"] == "Test"
    assert "user_id" in data

def test_get_user(client):
    create_response = client.post(
        "/users/",
        data={
            "email": "test2@example.com",
            "given_name": "Test2",
            "surname": "User2",
            "city": "Almaty",
            "phone_number": "+77071111111",
            "password": "password123"
        }
    )
    user_id = create_response.json()["user_id"]
    
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["email"] == "test2@example.com"

def test_get_users(client):
    client.post(
        "/users/",
        data={
            "email": "test3@example.com",
            "given_name": "Test3",
            "surname": "User3",
            "city": "Astana",
            "phone_number": "+77072222222",
            "password": "password123"
        }
    )
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_update_user(client):
    create_response = client.post(
        "/users/",
        data={
            "email": "test4@example.com",
            "given_name": "Test4",
            "surname": "User4",
            "city": "Astana",
            "phone_number": "+77073333333",
            "password": "password123"
        }
    )
    user_id = create_response.json()["user_id"]
    
    response = client.put(
        f"/users/{user_id}?given_name=Updated&city=Almaty"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["given_name"] == "Updated"
    assert data["city"] == "Almaty"

def test_delete_user(client):
    create_response = client.post(
        "/users/",
        data={
            "email": "test5@example.com",
            "given_name": "Test5",
            "surname": "User5",
            "city": "Astana",
            "phone_number": "+77074444444",
            "password": "password123"
        }
    )
    user_id = create_response.json()["user_id"]
    
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

