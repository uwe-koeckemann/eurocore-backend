import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from euro_core_backend.main import app, get_session

from euro_core_backend.test import test_entry_a, test_entry_b


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_team_tokens(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    team_entry_id = client.post("/entry/create/", json=test_entry_a).json()['id']
    response = client.post("/team-tokens/create", json={"id": team_entry_id, 'tokens': 0})
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == team_entry_id
    assert data["tokens"] == 0


def test_get_team_tokens(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    team_entry_id = client.post("/entry/create/", json=test_entry_a).json()['id']
    client.post("/team-tokens/create", json={"id": team_entry_id, 'tokens': 0})
    response = client.get(f"/team-tokens/get/{team_entry_id}")
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["tokens"] == 0
    assert data["id"] == team_entry_id


def test_get_team_tokens_by_id_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response = client.get(f"/team-tokens/get/{-1}")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_get_team_tokens_all_empty(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response = client.get(f"/team-tokens/get-all")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == []


def test_get_team_tokens_get_all_two_results(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    team_entry_id = client.post("/entry/create/", json=test_entry_a).json()['id']
    client.post("/team-tokens/create", json={"id": team_entry_id, 'tokens': 0})
    team_entry_id = client.post("/entry/create/", json=test_entry_b).json()['id']
    client.post("/team-tokens/create", json={"id": team_entry_id, 'tokens': 0})

    response = client.get(f"/team-tokens/get-all")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_team_tokens_update_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.put("/tag/update", json={"tokens": 100})
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_team_tokens_update_succeeds(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    entry_id = client.post("/entry/create/", json=test_entry_a).json()["id"]
    current_tokens = client.post("/team-tokens/create", json={"id": entry_id, 'tokens': 0}).json()
    current_tokens["tokens"] = 100
    response_update = client.put("/team-tokens/update", json=current_tokens)
    response_get = client.get(f"/team-tokens/get/{entry_id}")

    app.dependency_overrides.clear()
    assert response_update.status_code == 200
    assert response_update.json()["tokens"] == 100
    assert response_get.json()["tokens"] == 100



def test_team_tokens_delete_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.delete("/tag/delete/1")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_team_tokens_delete_succeeds(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    entry_id = client.post("/entry/create/", json=test_entry_a).json()["id"]
    current_tokens = client.post("/team-tokens/create", json={"id": entry_id, 'tokens': 0}).json()
    response_get_before = client.get(f"/team-tokens/get/{current_tokens['id']}")
    response_delete = client.delete(f"/team-tokens/delete/{current_tokens['id']}")
    response_after = client.get(f"/team-tokens/get/{current_tokens['id']}")

    app.dependency_overrides.clear()
    assert response_get_before.status_code == 200
    assert response_delete.status_code == 200
    assert response_after.status_code == 404

