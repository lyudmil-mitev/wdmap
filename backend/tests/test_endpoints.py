# test_main.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app, get_db
from app.models import Property, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from requests.auth import HTTPBasicAuth

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./wdmap_data.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_incorrect_login():
    response = client.post(
        "/login",
        auth=HTTPBasicAuth('admin', 'wrong_password')
    )
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_correct_login():
    response = client.post(
        "/login",
        auth=HTTPBasicAuth('admin', 'admin')
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

def test_get_10_properties(db_session: Session):
    response = client.get(
        "/properties?limit=10&offset=0",
        auth=HTTPBasicAuth('admin', 'admin')
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10

def test_filter_by_full_address(db_session: Session):
    response = client.get(
        "/properties?full_address=carpenter",
        auth=HTTPBasicAuth('admin', 'admin')
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for property in data:
        assert "carpenter" in property["full_address"].lower()

def test_filter_by_class_description(db_session: Session):
    response = client.get(
        "/properties?class_description=apartment",
        auth=HTTPBasicAuth('admin', 'admin')
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for property in data:
        assert "apartment" in property["class_description"].lower()

def test_filter_by_estimated_market_value(db_session: Session):
    response = client.get(
        "/properties?estimated_market_value=100000,2000000",
        auth=HTTPBasicAuth('admin', 'admin')
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for property in data:
        assert 100000 <= property["estimated_market_value"] <= 2000000

def test_invalid_filter_by_estimated_market_value(db_session: Session):
    response = client.get(
        "/properties?estimated_market_value=100000",
        auth=HTTPBasicAuth('admin', 'admin')
    )

    assert response.status_code == 422

def test_filter_by_building_sq_ft(db_session: Session):
    response = client.get(
        "/properties?building_sq_ft=1000,2000",
        auth=HTTPBasicAuth('admin', 'admin')
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for property in data:
        assert 1000 <= property["building_sq_ft"] <= 2000

def test_multiple_valid_filters(db_session: Session):
    response = client.get(
        "/properties?full_address=carpenter&class_description=apartment",
        auth=HTTPBasicAuth('admin', 'admin')
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for property in data:
        assert "carpenter" in property["full_address"].lower()
        assert "apartment" in property["class_description"].lower()

def test_get_property_by_id(db_session: Session):
    response = client.get(
        f"/properties/1",
        auth=HTTPBasicAuth('admin', 'admin')
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_limit_validation():
    response = client.get("/properties?limit=-1", auth=HTTPBasicAuth('admin', 'admin'))
    assert response.status_code == 422
    response = client.get("/properties?limit=2000", auth=HTTPBasicAuth('admin', 'admin'))
    assert response.status_code == 422

def test_offset_validation():
    response = client.get("/properties?offset=-1", auth=HTTPBasicAuth('admin', 'admin'))
    assert response.status_code == 422