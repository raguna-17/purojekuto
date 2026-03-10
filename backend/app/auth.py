import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .db import get_db
from .models import User


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


# -----------------------
# JWT トークン生成
# -----------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# -----------------------
# パスワードハッシュ
# -----------------------
def hash_password(password: str) -> str:
    return argon2.hash(password)


# -----------------------
# パスワード検証
# -----------------------
def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return argon2.verify(
        plain_password,
        hashed_password
    )


# -----------------------
# 現在ユーザー取得
# -----------------------
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id: Optional[str] = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )

    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user