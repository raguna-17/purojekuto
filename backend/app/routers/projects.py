from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db import get_db
from ..models import Project
from ..schemas import ProjectCreate, ProjectRead
from ..auth import get_current_user
from ..models import User

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

# ----------------------
# プロジェクト作成
# ----------------------
@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_project = Project(
        name=project_in.name,
        description=project_in.description,
        owner_id=current_user.id
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return ProjectRead.from_orm(new_project)


# ----------------------
# 自分のプロジェクト一覧取得
# ----------------------
@router.get("/", response_model=list[ProjectRead])
async def read_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Project).where(Project.owner_id == current_user.id)
    )

    projects = result.scalars().all()

    return [ProjectRead.from_orm(p) for p in projects]

    
# ----------------------
# プロジェクト取得（ID指定）
# ----------------------
@router.get("/{project_id}", response_model=ProjectRead)
async def read_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRead.from_orm(project)


# ----------------------
# プロジェクト削除
# ----------------------
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project)
    await db.commit()
    return