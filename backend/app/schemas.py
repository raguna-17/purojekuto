from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ------------------------
# User
# ------------------------
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ログイン用スキーマ
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ------------------------
# Project
# ------------------------
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ------------------------
# Task
# ------------------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    priority: Optional[int] = 1
    


class TaskCreate(TaskBase):
    project_id: int


class TaskRead(TaskBase):
    id: int
    project_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ------------------------
# Comment
# ------------------------
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    task_id: int
  


class CommentRead(CommentBase):
    id: int
    task_id: int
    author_id: int
    created_at: datetime

    model_config = {"from_attributes": True}