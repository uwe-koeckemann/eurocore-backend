import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from euro_core_backend.main import app, get_session

from euro_core_backend.test import test_entry_a, test_entry_b, test_team_a, test_team_b


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_module_usage(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    offer_team_id = client.post("/entry/create/", json=test_team_a).json()['id']
    consumer_team_id = client.post("/entry/create/", json=test_team_b).json()['id']
    module_id = client.post("/entry/create/", json=test_entry_a).json()['id']
    offer_id = client.post("/module-offer/create", json={
        "team_id": offer_team_id,
        "module_id": module_id,
        "cost": 1000,
        "integration_support": True,
        "integration_cost": 100}).json()["id"]
    response = client.post("/module-usage/create", json={
        "consumer_team_id": consumer_team_id,
        "module_offer_id": offer_id,
        "bought": True,
        "bought_support": False,
        "using": True,
        "rating": 10,
        "review": "Great!"
    })

    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["consumer_team_id"] == consumer_team_id
    assert data["module_offer_id"] == offer_id
    assert data["bought"]
    assert not data["bought_support"]
    assert data["using"]
    assert data["rating"] == 10
    assert data["review"] == "Great!"


def test_get_module_usage(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    offer_team_id = client.post("/entry/create/", json=test_team_a).json()['id']
    consumer_team_id = client.post("/entry/create/", json=test_team_b).json()['id']
    module_id = client.post("/entry/create/", json=test_entry_a).json()['id']
    offer_id = client.post("/module-offer/create", json={
        "team_id": offer_team_id,
        "module_id": module_id,
        "cost": 1000,
        "integration_support": True,
        "integration_cost": 100}).json()["id"]
    response = client.post("/module-usage/create", json={
        "consumer_team_id": consumer_team_id,
        "module_offer_id": offer_id,
        "bought": True,
        "bought_support": False,
        "using": True,
        "rating": 10,
        "review": "Great!"
    })
    response_get = client.get(f"/module-usage/get/{response.json()['id']}")
    app.dependency_overrides.clear()
    data = response_get.json()
    assert response_get.status_code == 200
    assert data["consumer_team_id"] == consumer_team_id
    assert data["module_offer_id"] == offer_id
    assert data["bought"]
    assert not data["bought_support"]
    assert data["using"]
    assert data["rating"] == 10
    assert data["review"] == "Great!"


def test_get_module_usage_id_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response = client.get(f"/module-usage/get/{-1}")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_get_module_usage_all_empty(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)

    response = client.get(f"/module-usage/get-all")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == []


def test_get_module_offer_get_all_two_results(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    offer_team_id = client.post("/entry/create/", json=test_team_a).json()['id']
    consumer_team_id = client.post("/entry/create/", json=test_team_b).json()['id']
    module_id = client.post("/entry/create/", json=test_entry_a).json()['id']
    offer_id = client.post("/module-offer/create", json={
        "team_id": offer_team_id,
        "module_id": module_id,
        "cost": 1000,
        "integration_support": True,
        "integration_cost": 100}).json()["id"]
    client.post("/module-usage/create", json={
        "consumer_team_id": consumer_team_id,
        "module_offer_id": offer_id,
        "bought": True,
        "bought_support": False,
        "using": True,
        "rating": 10,
        "review": "Great!"
    })

    response = client.get(f"/module-usage/get-all")
    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_module_usage_update_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.put("/module-usage/update", json={"tokens": 100})
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_module_usage_update_succeeds(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    offer_team_id = client.post("/entry/create/", json=test_team_a).json()['id']
    consumer_team_id = client.post("/entry/create/", json=test_team_b).json()['id']
    module_id = client.post("/entry/create/", json=test_entry_a).json()['id']
    offer_id = client.post("/module-offer/create", json={
        "team_id": offer_team_id,
        "module_id": module_id,
        "cost": 1000,
        "integration_support": True,
        "integration_cost": 100}).json()["id"]
    current = client.post("/module-usage/create", json={
        "consumer_team_id": consumer_team_id,
        "module_offer_id": offer_id,
        "bought": True,
        "bought_support": False,
        "using": True,
        "rating": 10,
        "review": "Great!"
    }).json()
    current["bought_support"] = True
    current["review"] = "Great module and support!"
    response_update = client.put("/module-usage/update", json=current)
    response_get = client.get(f"/module-usage/get/{current['id']}")

    app.dependency_overrides.clear()
    data = response_get.json()
    assert response_update.status_code == 200
    assert data["consumer_team_id"] == consumer_team_id
    assert data["module_offer_id"] == offer_id
    assert data["bought"]
    assert data["bought_support"]
    assert data["using"]
    assert data["rating"] == 10
    assert data["review"] == "Great module and support!"


def test_module_usage_delete_fails(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    response = client.delete("/module-usage/delete/1")
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_module_usage_delete_succeeds(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    offer_team_id = client.post("/entry/create/", json=test_team_a).json()['id']
    consumer_team_id = client.post("/entry/create/", json=test_team_b).json()['id']
    module_id = client.post("/entry/create/", json=test_entry_a).json()['id']
    offer_id = client.post("/module-offer/create", json={
        "team_id": offer_team_id,
        "module_id": module_id,
        "cost": 1000,
        "integration_support": True,
        "integration_cost": 100}).json()["id"]
    usage_id = client.post("/module-usage/create", json={
        "consumer_team_id": consumer_team_id,
        "module_offer_id": offer_id,
        "bought": True,
        "bought_support": False,
        "using": True,
        "rating": 10,
        "review": "Great!"
    }).json()["id"]
    response_get_before = client.get(f"/module-usage/get/{usage_id}")
    response_delete = client.delete(f"/module-usage/delete/{usage_id}")
    response_get_after = client.get(f"/module-usage/get/{usage_id}")
    app.dependency_overrides.clear()
    assert response_get_before.status_code == 200
    assert response_delete.status_code == 200
    assert response_get_after.status_code == 404
