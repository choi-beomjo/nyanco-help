import os
import sys
from pathlib import Path


# 프로젝트 루트 디렉토리를 PYTHONPATH에 추가
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# app 디렉토리를 PYTHONPATH에 추가
app_path = str(Path(project_root) / "app")
sys.path.insert(0, app_path)

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model.base import Base
from app.api.deps import get_crud

# DB 파일 경로를 절대 경로로 설정
DB_PATH = os.path.abspath("myapi.db")
print(f"\nDatabase path in conftest.py: {DB_PATH}")

# SQLAlchemy URL 설정
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
print(f"SQLAlCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 세션 생성
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def app():
    from app.main import app
    return app

@pytest.fixture(scope="session")
def client(app):
    return TestClient(app)

@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        #Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def crud(db):
    return get_crud(db)

@pytest.fixture(scope="function")
def auth_headers():
    # 테스트용 인증 토큰 생성
    return {"Authorization": "Bearer test_token"}
