import pytest
from fastapi import HTTPException
from app.api.domain.character.utils import (
    add_character_to_db,
    get_characters_from_db,
    get_duplicate_character,
    get_character_from_db,
    update_character_from_db,
    delete_character_from_db
)
from app.api.domain.character.models import Character
from app.api.domain.skill.models import Skill
from app.api.domain.property.models import Property

@pytest.fixture
def mock_character_data():
    return {
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
        "skills": [Skill(id=1, name="Strong")],  # 스킬 ID 리스트
        "properties": [Property(id=1, name="Red")]  # 속성 ID 리스트
    }

@pytest.fixture
def mock_character_data2():
    return {
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
        "skills": [dict(id=1, name="Strong")],  # 스킬 ID 리스트
        "properties": [dict(id=1, name="Red")]  # 속성 ID 리스트
    }

@pytest.fixture
def mock_character_data3():
    return {
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
        "skills": [1],  # 스킬 ID 리스트
        "properties": [1]  # 속성 ID 리스트
    }

@pytest.fixture
def mock_skill():
    return Skill(id=1, name="Test Skill")

@pytest.fixture
def mock_property():
    return Property(id=1, name="Test Property")

class TestCharacterUtils:
    def test_add_character_to_db(self, crud, mock_character_data3):
        # 스킬과 속성 모의 객체 설정
        #crud.read = lambda model, filters, single=False: mock_skill if model == Skill else mock_property
        
        # 캐릭터 추가
        add_character_to_db(mock_character_data3, crud)
        
        # 캐릭터가 제대로 추가되었는지 확인
        characters = crud.read_all(Character)
        assert len(characters) > 0
        assert characters[-1].name == mock_character_data3["name"]

    def test_get_characters_from_db(self, crud, mock_character_data):
        # 테스트 데이터 설정
        test_character = Character(**mock_character_data)
        crud.read_all = lambda model, **kwargs: [test_character]
        
        # 캐릭터 조회
        characters = get_characters_from_db(crud)
        assert len(characters) == 1
        assert characters[0].name == mock_character_data["name"]

    def test_get_duplicate_character(self, crud, mock_character_data):
        # 중복 캐릭터 검사
        crud.read = lambda model, filters: Character(**mock_character_data)
        
        result = get_duplicate_character({"name": "Test Character"}, crud)
        assert result is not None
        assert result.name == "Test Character"

    def test_get_character_from_db_success(self, crud, mock_character_data):
        # 캐릭터 조회 성공 케이스
        test_character = Character(**mock_character_data)
        crud.read = lambda model, filters, relationships=None, single=False: test_character
        
        character = get_character_from_db(1, crud)
        assert character is not None
        assert character.name == mock_character_data["name"]

    def test_get_character_from_db_not_found(self, crud):
        # 캐릭터 조회 실패 케이스
        crud.read = lambda model, filters, relationships=None, single=False: None
        
        with pytest.raises(HTTPException) as exc_info:
            get_character_from_db(999, crud)
        assert exc_info.value.status_code == 404

    def test_update_character_from_db_success(self, crud, mock_character_data, mock_skill, mock_property):
        # 캐릭터 업데이트 성공 케이스
        test_character = Character(**mock_character_data)
        crud.read = lambda model, filters=None, single=False: mock_skill if model == Skill else mock_property
        crud.update = lambda model, id, **kwargs: test_character
        
        updated_character = update_character_from_db(1, mock_character_data, crud)
        assert updated_character is not None
        assert updated_character.name == mock_character_data["name"]

    def test_update_character_from_db_not_found(self, crud, mock_character_data2):
        # 캐릭터 업데이트 실패 케이스
        crud.update = lambda model, id, **kwargs: None
        
        with pytest.raises(HTTPException) as exc_info:
            update_character_from_db(999, mock_character_data2, crud)
        assert exc_info.value.status_code == 404

    def test_delete_character_from_db_success(self, crud, mock_character_data):
        # 캐릭터 삭제 성공 케이스
        test_character = Character(**mock_character_data)
        crud.delete = lambda model, id: test_character
        
        deleted_character = delete_character_from_db(1, crud)
        assert deleted_character is not None
        assert deleted_character.name == mock_character_data["name"]

    def test_delete_character_from_db_not_found(self, crud):
        # 캐릭터 삭제 실패 케이스
        crud.delete = lambda model, id: None
        
        with pytest.raises(HTTPException) as exc_info:
            delete_character_from_db(999, crud)
        assert exc_info.value.status_code == 404
