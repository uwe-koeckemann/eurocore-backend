import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from euro_core_backend.main import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_tag(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response = client.post(
        "/tag/create", json={"name": "Tag_A"}
    )
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Tag_A"
    assert data["id"] is not None


def test_get_tag_by_id(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response_post = client.post("/tag/create", json={"name": "Tag_B"})
    tag_id = response_post.json()["id"]

    response = client.get(
        f"/tag/get/{tag_id}"
    )
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Tag_B"
    assert data["id"] == tag_id


def test_get_tag_by_id_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response = client.get(
        f"/tag/get/-1"
    )
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_get_tag_by_name(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response_post = client.post("/tag/create", json={"name": "Tag_B"})
    tag_id = response_post.json()["id"]

    response = client.get(
        f"/tag/get-by-name/Tag_B"
    )
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Tag_B"
    assert data["id"] == tag_id


def test_get_tag_by_name_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session

    client = TestClient(app)

    response = client.get(
        f"/tag/get-by-name/Tag_Not_In_DB"
    )
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_get_tag_get_all_empty(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response = client.get(
        f"/tag/get-all"
    )
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == []


def test_get_tag_get_all_two_results(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    client.post("/tag/create", json={"name": "Tag_A"})
    client.post("/tag/create", json={"name": "Tag_B"})

    response = client.get(f"/tag/get-all")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_tag_update_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.put("/tag/update", json={"name": "New_Name"})
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_tag_update_succeeds(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response_create = client.post("/tag/create", json={"name": "Tag_A"})
    tag_current = response_create.json()
    tag_current["name"] = "New_Name"
    response_update = client.put("/tag/update", json=tag_current)

    response_get = client.get(f"/tag/get/{tag_current['id']}")
    app.dependency_overrides.clear()
    assert response_update.status_code == 200
    assert response_update.json()["name"] == "New_Name"
    assert response_get.json()["name"] == "New_Name"


def test_tag_delete_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.delete("/tag/delete/1")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_tag_delete_succeeds(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response_create = client.post("/tag/create", json={"name": "Tag_A"})
    tag_current = response_create.json()
    response_get_before = client.get(f"/tag/get/{tag_current['id']}")
    response_delete = client.delete(f"/tag/delete/{tag_current['id']}")
    response_after = client.get(f"/tag/get/{tag_current['id']}")

    app.dependency_overrides.clear()
    assert response_get_before.status_code == 200
    assert response_delete.status_code == 200
    assert response_after.status_code == 404

