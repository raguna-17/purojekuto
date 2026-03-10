from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db import get_db
from ..models import User
from ..schemas import UserRead, UserCreate, UserLogin
from ..auth import get_current_user, hash_password

router = APIRouter(prefix="/api/v1/users", tags=["users"])

# ----------------------
# 自分の情報取得
# ----------------------
@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    # Pydanticモデルに変換して返す
    return UserRead.model_validate(user)



# ----------------------
@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user_in.password)
    new_user = User(email=user_in.email, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return UserRead.from_orm(new_user)


@router.post("/login")
async def login(
    user_in: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    from ..auth import verify_password, create_access_token

    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }