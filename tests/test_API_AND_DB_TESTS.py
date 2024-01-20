import pytest
from main import app, APIKey, get_db, get_path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scheme import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

LocalTestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = LocalTestingSession()
        yield db
    finally:
        db.close()

def override_get_path():
    yield "tests/testing_images/"

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_path] = override_get_path
client = TestClient(app)

headers = {"access_token": APIKey, "Username":"oliver"}
user = {"username":"oliver"}

@pytest.fixture(autouse=True)
def reset_database():
    print("Running reset_database fixture")
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("Dropped and recreated tables")
    except Exception as e:
        print("Error resetting database:", e)

def test_read_item():
    response = client.get("/api/APIKey")
    assert response.status_code == 200
    assert response.json() == {"APIKey": APIKey}

def test_register():
    global headers
    response = client.post("/api/register", json = user, headers = headers) 

    assert response.status_code == 200, response.json()
    assert response.json() == {
            'status': 'success',
            'message': 'User registered successfully'
        }
    
def test_login():
    test_register()

    response = client.post("/api/login", json = user, headers = headers) 

    assert response.status_code == 200
    assert response.json() == {
                'status': 'success',
                'message': 'User logged in successfully'
            }
    
def test_sending_primary_phase():
    response = client.post("/api/register", json = user, headers = headers) 

    assert response.status_code == 200, response.json()

    file = open("tests/testing_images/desalle_21.9_2B.jpg", "rb")
    file = {"file": file}

    response = client.post("/api/upload", headers = headers, files = file)
    assert(response.status_code == 200), response.json()
    phase_info = response.json()["phase_info"]
    assert(phase_info["map_name"] == "Desalle")
