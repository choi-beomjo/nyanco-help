import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.domain.enemy.api import router as enemy_router
from app.api.deps import get_crud, CRUD, admin_required
from app.db.crud.crud import SessionLocal

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(enemy_router, prefix="/api/enemy")
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

@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test_token"}

def test_get_enemy_list(client):
    response = client.get("/api/enemy/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_enemy(client, auth_headers):
    enemy_data = {
        "name": "Test Enemy",
        "atk": 100,
        "hp": 1000,
        "range": 1,
        "kb": 1,
        "dps": 100,
        "money": 100,
        "speed": 1,
        "tba": 1,
        "target": "Single",
        "atk_sec": 1,
        "skills": [],
        "properties": []
    }
    
    response = client.post("/api/enemy", json=enemy_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "success"

def test_get_enemy(client, auth_headers):
    # 먼저 적을 생성
    enemy_data = {
        "name": "Test Enemy 2",
        "atk": 100,
        "hp": 1000,
        "range": 1,
        "kb": 1,
        "dps": 100,
        "money": 100,
        "speed": 1,
        "tba": 1,
        "target": "Single",
        "atk_sec": 1,
        "skills": [],
        "properties": []
    }
    
    post_response = client.post("/api/enemy", json=enemy_data, headers=auth_headers)
    #assert post_response.status_code == 200
    
    # 생성된 적 조회
    response = client.get(f"/api/enemy/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Enemy 2"

def test_update_enemy(client, auth_headers):
    # 먼저 적을 생성
    enemy_data = {
        "name": "Test Enemy 3",
        "atk": 100,
        "hp": 1000,
        "range": 1,
        "kb": 1,
        "dps": 100,
        "money": 100,
        "speed": 1,
        "tba": 1,
        "target": "Single",
        "atk_sec": 1,
        "skills": [],
        "properties": []
    }
    
    post_response = client.post("/api/enemy", json=enemy_data, headers=auth_headers)
    assert post_response.status_code == 200
    
    # 적 정보 업데이트
    update_data = {
        "name": "Updated Enemy",
        "atk": 200,
        "hp": 2000,
        "range": 2,
        "kb": 2,
        "dps": 200,
        "money": 200,
        "speed": 2,
        "tba": 2,
        "target": "Single",
        "atk_sec": 2,
        "skills": [],
        "properties": []
    }
    
    response = client.put("/api/enemy/1", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Enemy"

def test_delete_enemy(client, auth_headers):
    # 먼저 적을 생성
    enemy_data = {
        "name": "Test Enemy 4",
        "atk": 100,
        "hp": 1000,
        "range": 1,
        "kb": 1,
        "dps": 100,
        "money": 100,
        "speed": 1,
        "tba": 1,
        "target": "Single",
        "atk_sec": 1,
        "skills": [],
        "properties": []
    }
    
    post_response = client.post("/api/enemy", json=enemy_data, headers=auth_headers)
    assert post_response.status_code == 200
    
    # 적 삭제
    response = client.delete("/api/enemy/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "sucess"

def test_search_enemies(client):
    search_data = {
        "skills": [],
        "properties": []
    }
    
    response = client.post("/api/enemy/search", json=search_data)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
