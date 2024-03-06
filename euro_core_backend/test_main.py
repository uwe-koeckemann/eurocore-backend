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
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
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
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
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
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    response = client.get(
        f"/tag/get/-1"
    )
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_get_tag_by_name(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
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
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)

    response = client.get(
        f"/tag/get-by-name/Tag_Not_In_DB"
    )
    app.dependency_overrides.clear()
    assert response.status_code == 404
