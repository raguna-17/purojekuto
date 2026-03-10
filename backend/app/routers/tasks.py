from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db import get_db
from ..models import Task, Project, User
from ..schemas import TaskCreate, TaskRead
from ..auth import get_current_user

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

# ----------------------
# タスク作成
# ----------------------
@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == task_in.project_id, Project.owner_id == current_user.id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by user")

    new_task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority,
        due_date=task_in.due_date,
        project_id=task_in.project_id
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return TaskRead.from_orm(new_task)

# ----------------------
# 自分のプロジェクト内のタスク一覧取得
# ----------------------
@router.get("/project/{project_id}", response_model=list[TaskRead])
async def read_tasks_by_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by user")

    result = await db.execute(select(Task).where(Task.project_id == project_id))
    tasks = result.scalars().all()
    return [TaskRead.from_orm(t) for t in tasks]



# ----------------------
# タスク削除
# ----------------------
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    result = await db.execute(select(Project).where(Project.id == task.project_id, Project.owner_id == current_user.id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    await db.delete(task)
    await db.commit()
    return