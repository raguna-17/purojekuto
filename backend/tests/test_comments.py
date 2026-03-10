import pytest


@pytest.mark.asyncio
async def create_project(client):
    res = await client.post(
        "/api/v1/projects/",
        json={"name": "Project", "description": "desc"}
    )
    return res.json()["id"]


@pytest.mark.asyncio
async def create_task(client, project_id):
    res = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Task",
            "description": "desc",
            "project_id": project_id
        }
    )
    return res.json()["id"]


@pytest.mark.asyncio
async def test_create_comment(client):

    project_id = await create_project(client)
    task_id = await create_task(client, project_id)

    res = await client.post(
        "/api/v1/comments/",
        json={
            "content": "hello",
            "task_id": task_id
        }
    )

    assert res.status_code == 201
    assert res.json()["content"] == "hello"


@pytest.mark.asyncio
async def test_get_comments_by_task(client):

    project_id = await create_project(client)
    task_id = await create_task(client, project_id)

    await client.post(
        "/api/v1/comments/",
        json={
            "content": "test comment",
            "task_id": task_id
        }
    )

    res = await client.get(f"/api/v1/comments/task/{task_id}")

    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.asyncio
async def test_delete_comment(client):

    project_id = await create_project(client)
    task_id = await create_task(client, project_id)

    comment = await client.post(
        "/api/v1/comments/",
        json={
            "content": "delete me",
            "task_id": task_id
        }
    )

    comment_id = comment.json()["id"]

    res = await client.delete(f"/api/v1/comments/{comment_id}")

    assert res.status_code == 204