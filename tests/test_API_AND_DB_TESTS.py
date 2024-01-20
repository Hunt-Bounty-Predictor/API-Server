from main import app, APIKey
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scheme import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

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

app.dependency_overrides['get_db'] = override_get_db
client = TestClient(app)

def test_read_item():
    response = client.get("/api/APIKey")
    assert response.status_code == 200
    assert response.json() == {"APIKey": APIKey}
