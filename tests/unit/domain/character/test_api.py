# tests/unit/domain/character/test_api.py
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.domain.character.api import router as character_router
from app.api.deps import get_crud, CRUD, admin_required
from app.db.crud.crud import SessionLocal


# 테스트용 앱 생성
@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(character_router, prefix="/api/character")
    return app

# 의존성 오버라이드
def override_get_crud():
    db = SessionLocal()
    try:
        yield CRUD(db)
    finally:
        db.close()

# admin_required 의존성 오버라이드
def override_admin_required():
    return {"id": 1, "username": "admin", "is_admin": True}

@pytest.fixture
def client(app):
    # 의존성 오버라이드 설정
    app.dependency_overrides[get_crud] = override_get_crud
    app.dependency_overrides[admin_required] = override_admin_required
    return TestClient(app)

def test_get_character_list(client):
    response = client.get("/api/character/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_post_character(client):
    character_data = {
        "name": "Test Character",
        "atk": 100,
        "hp": 1000,
        "range": 1,
        "grade": "Rare",
        "dps": 100,
        "cost": 100,
        "kb": 1,
        "target": "Single",
        "tba": 1.0,
        "atk_sec": 1.0,
        "speed": 1,
        "spawn": 1.0,
        "skills": [],
        "properties": []
    }
    
    response = client.post("/api/character", json=character_data)
    assert response.status_code == 200
    assert response.json()["msg"] == "success"

def test_get_character(client):
    # 먼저 캐릭터를 생성
    character_data = {
        "name": "Test Character 2",
        "atk": 100,
        "hp": 1000,
        "range": 1,
        "grade": "Rare",
        "dps": 100,
        "cost": 100,
        "kb": 1,
        "target": "Single",
        "tba": 1.0,
        "atk_sec": 1.0,
        "speed": 1,
        "spawn": 1.0,
        "skills": [],
        "properties": []
    }
    
    post_response = client.post("/api/character", json=character_data)
    #assert post_response.status_code == 200
    
    # 생성된 캐릭터 조회
    response = client.get(f"/api/character/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Cat"
