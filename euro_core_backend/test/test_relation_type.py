import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from euro_core_backend.main import app, get_session
from euro_core_backend.test import test_relation_a
from euro_core_backend.test import test_relation_b

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_relation_type(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response = client.post(
        "/relation_type/create", json=test_relation_a
    )
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "relation_a"
    assert data["inverse_name"] == "relation_a_inv"
    assert data["topic"] == "Relation A"
    assert data["inverse_topic"] == "Inverse of Relation A"
    assert data["id"] is not None


def test_get_relation_type_by_id(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response_post = client.post("/relation_type/create", json=test_relation_a)
    relation_type_id = response_post.json()["id"]
    response = client.get(f"/relation_type/get/{relation_type_id}")
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "relation_a"
    assert data["id"] == relation_type_id


def test_get_relation_type_by_id_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.get(f"/relation_type/get/-1")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_get_relation_type_by_name(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response_post = client.post("/relation_type/create", json=test_relation_a)
    relation_type_id = response_post.json()["id"]

    response = client.get(f"/relation_type/get-by-name/relation_a")
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "relation_a"
    assert data["id"] == relation_type_id


def test_get_relation_type_by_name_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.get("/relation_type/get-by-name/Tag_Not_In_DB")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_get_relation_type_get_all_empty(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.get(f"/relation_type/get-all")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == []


def test_get_relation_type_get_all_two_results(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    client.post("/relation_type/create", json=test_relation_a)
    client.post("/relation_type/create", json=test_relation_b)
    response = client.get(f"/relation_type/get-all")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_relation_type_update_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.put("/relation_type/update", json={"name": "New_Name"})
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_relation_type_update_succeeds(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response_create = client.post("/relation_type/create", json=test_relation_a)
    relation_type_current = response_create.json()
    relation_type_current["name"] = "New_Name"
    response_update = client.put("/relation_type/update", json=relation_type_current)
    response_get = client.get(f"/relation_type/get/{relation_type_current['id']}")
    app.dependency_overrides.clear()
    assert response_update.status_code == 200
    assert response_update.json()["name"] == "New_Name"
    assert response_get.json()["name"] == "New_Name"


def test_relation_type_delete_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.delete("/relation_type/delete/1")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_relation_type_delete_succeeds(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response_create = client.post("/relation_type/create", json=test_relation_a)
    relation_type_current = response_create.json()
    response_get_before = client.get(f"/relation_type/get/{relation_type_current['id']}")
    response_delete = client.delete(f"/relation_type/delete/{relation_type_current['id']}")
    response_after = client.get(f"/relation_type/get/{relation_type_current['id']}")

    app.dependency_overrides.clear()
    assert response_get_before.status_code == 200
    assert response_delete.status_code == 200
    assert response_after.status_code == 404

