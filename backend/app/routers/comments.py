from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db import get_db
from ..models import Comment, Task, User
from ..schemas import CommentCreate, CommentRead
from ..auth import get_current_user

router = APIRouter(prefix="/api/v1/comments", tags=["comments"])


# ----------------------
# タスクごとのコメント取得
# ----------------------
@router.get("/task/{task_id}", response_model=list[CommentRead])
async def read_comments_by_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    result = await db.execute(select(Comment).where(Comment.task_id == task_id))
    comments = result.scalars().all()
    return [CommentRead.from_orm(c) for c in comments]


# ----------------------
# コメント投稿
# ----------------------
@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_in: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # タスク存在確認
    result = await db.execute(
        select(Task).where(Task.id == comment_in.task_id)
    )
    task = result.scalars().first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # コメント作成
    new_comment = Comment(
        content=comment_in.content,
        task_id=comment_in.task_id,
        author_id=current_user.id
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return CommentRead.from_orm(new_comment)


# ----------------------
# コメント削除
# ----------------------
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalars().first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    await db.delete(comment)
    await db.commit()
    return