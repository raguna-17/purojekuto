import pytest


@pytest.fixture
async def project_id(client):
    res = await client.post(
        "/api/v1/projects/",
        json={"name": "TaskProject", "description": "desc"}
    )
    return res.json()["id"]


@pytest.mark.asyncio
async def test_create_task(client, project_id):

    res = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Test Task",
            "description": "task desc",
            "status": "todo",
            "priority": 1,
            "project_id": project_id
        }
    )

    assert res.status_code == 201
    assert res.json()["title"] == "Test Task"


@pytest.mark.asyncio
async def test_create_task_project_not_found(client):

    res = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Task",
            "description": "desc",
            "project_id": 999
        }
    )

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_get_tasks_by_project(client, project_id):

    await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Task1",
            "description": "desc",
            "project_id": project_id
        }
    )

    res = await client.get(f"/api/v1/tasks/project/{project_id}")

    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.asyncio
async def test_delete_task(client, project_id):

    task = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "TaskDelete",
            "description": "desc",
            "project_id": project_id
        }
    )

    task_id = task.json()["id"]

    res = await client.delete(f"/api/v1/tasks/{task_id}")

    assert res.status_code == 204


@pytest.mark.asyncio
async def test_get_tasks_project_not_found(client):

    res = await client.get("/api/v1/tasks/project/999")

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_found(client):

    res = await client.delete("/api/v1/tasks/999")

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_task_not_owner(client, db_session):

    project = await client.post(
        "/api/v1/projects/",
        json={"name": "Project1", "description": "desc"}
    )
    project_id = project.json()["id"]

    task = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Task",
            "description": "desc",
            "project_id": project_id
        }
    )

    task_id = task.json()["id"]

    from app.models import User
    from app.auth import hash_password
    from app.auth import get_current_user
    from app.main import app

    other_user = User(
        email="other@example.com",
        hashed_password=hash_password("password"),
        is_active=True
    )

    db_session.add(other_user)
    await db_session.commit()
    await db_session.refresh(other_user)

    async def override_user():
        return other_user

    app.dependency_overrides[get_current_user] = override_user

    res = await client.delete(f"/api/v1/tasks/{task_id}")

    assert res.status_code == 403

    app.dependency_overrides.clear()