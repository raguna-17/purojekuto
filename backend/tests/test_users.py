import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/users/",
        json={"email": "newuser@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, test_user):
    response = await client.post(
        "/api/v1/users/login",
        json={
            "email": test_user.email,
            "password": "password123"
        }
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user):
    from app.auth import create_access_token

    token = create_access_token({"sub": str(test_user.id)})
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/v1/users/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email



@pytest.mark.asyncio
async def test_create_user_duplicate_email(client, test_user):
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": test_user.email,
            "password": "password123"
        }
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_user_not_found(client):
    response = await client.post(
        "/api/v1/users/login",
        json={
            "email": "unknown@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_user_wrong_password(client, test_user):
    response = await client.post(
        "/api/v1/users/login",
        json={
            "email": test_user.email,
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401