import pytest
from httpx import AsyncClient
from app.auth import create_access_token


# -------------------------
# 正常系
# -------------------------

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):

    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "newuser@example.com",
            "password": "password123"
        }
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

    token = create_access_token({"sub": str(test_user.id)})

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = await client.get("/api/v1/users/me", headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == test_user.email


# -------------------------
# 異常系
# -------------------------

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
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email,password",
    [
        ("unknown@example.com", "password123"),  # ユーザー不存在
        ("test@example.com", "wrongpassword"),   # パスワード違い
    ],
)
async def test_login_failures(client, test_user, email, password):

    # test_user の email を利用するケース
    if email == "test@example.com":
        email = test_user.email

    response = await client.post(
        "/api/v1/users/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 401