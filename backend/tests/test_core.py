import pytest
from jose import jwt

from app.models import User
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM
)


@pytest.mark.asyncio
async def test_password_hashing():
    plain = "password123"
    hashed = hash_password(plain)

    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("wrong", hashed) is False


@pytest.mark.asyncio
async def test_user_creation(db_session):

    user = User(
        email="coretest@example.com",
        hashed_password=hash_password("secret"),
        is_active=True
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.email == "coretest@example.com"


@pytest.mark.asyncio
async def test_access_token(test_user):

    token = create_access_token({"sub": str(test_user.id)})

    assert token is not None


@pytest.mark.asyncio
async def test_access_token_payload(test_user):

    token = create_access_token({"sub": str(test_user.id)})

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert payload["sub"] == str(test_user.id)