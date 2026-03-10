import pytest


@pytest.mark.asyncio
async def test_create_project(client):
    res = await client.post(
        "/api/v1/projects/",
        json={
            "name": "Test Project",
            "description": "sample project"
        }
    )

    assert res.status_code == 201
    data = res.json()

    assert data["name"] == "Test Project"
    assert data["description"] == "sample project"
    assert "id" in data


@pytest.mark.asyncio
async def test_read_project(client):
    create = await client.post(
        "/api/v1/projects/",
        json={"name": "Project1", "description": "desc"}
    )

    project_id = create.json()["id"]

    res = await client.get(f"/api/v1/projects/{project_id}")

    assert res.status_code == 200
    assert res.json()["id"] == project_id


@pytest.mark.asyncio
async def test_read_project_not_found(client):
    res = await client.get("/api/v1/projects/999")

    assert res.status_code == 404


@pytest.mark.asyncio
async def test_delete_project(client):
    create = await client.post(
        "/api/v1/projects/",
        json={"name": "DeleteMe", "description": "temp"}
    )

    project_id = create.json()["id"]

    res = await client.delete(f"/api/v1/projects/{project_id}")

    assert res.status_code == 204