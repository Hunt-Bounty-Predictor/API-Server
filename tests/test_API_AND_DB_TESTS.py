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
    except Exception as e:
        print("Error getting database:", e)
    finally:
        db.close()

def override_get_path():
    yield "tests/data/"

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

@pytest.fixture()
def register():
    response = client.post("/api/register", json = user, headers = headers) 

    assert response.status_code == 200, response.json()
    assert response.json() == {
            'status': 'success',
            'message': 'User registered successfully'
        }

def test_read_item():
    response = client.get("/api/APIKey")
    assert response.status_code == 200
    assert response.json() == {"APIKey": APIKey}

def test_register():
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

def test_sending_two_images(register):
    file = open("tests/sequential_images/desalle_no_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == True)

    file = open("tests/sequential_images/desalle_one_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == False)

def test_sending_entire_map(register):
    file = open("tests/sequential_images/desalle_no_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == True)

    file = open("tests/sequential_images/desalle_one_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == False)

    file = open("tests/sequential_images/desalle_two_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == False)

    file = open("tests/sequential_images/desalle_three_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == False)

def test_sending_two_same_phases(register):
    file = open("tests/sequential_images/desalle_no_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == True)

    file = open("tests/sequential_images/desalle_one_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == False)

    file = open("tests/sequential_images/desalle_one_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 500), response.json()
    assert(response.json()["detail"]['status'] == "failure")
    assert(response.json()["detail"]['message'] == "To many compounds compared to your last image. Did you miss some images?")

def test_sending_a_diff_map(register):
    file = open("tests/sequential_images/desalle_no_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 200), response.json()
    assert(response.json()["phase_info"]["map_name"] == "Desalle")
    assert(response.json()["phase_info"]["is_primary"] == True)

    file = open("tests/sequential_images/desalle_one_clues_21_9_qhd.jpg", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    file = open("tests/testing_images/stillwater_16.9_1B.png", "rb")
    file = {"file": file}
    response = client.post("/api/upload", headers = headers, files = file)

    assert(response.status_code == 500), response.json()
    assert(response.json()["detail"]['message'] == "The map of the image does not match the map of the last intial image you sent.")