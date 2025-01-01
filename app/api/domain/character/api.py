from fastapi import APIRouter, Depends
from ...tags import Tags
from utils.msg.msg import Msg
from .utils import *
from .schemas import *
from .models import *
from ...deps import get_current_user, get_crud, CRUD, admin_required
from ..skill.schemas import SkillInfo


router = APIRouter(tags=[Tags.character])


@router.get("/list")
def get_character_list(crud: CRUD = Depends(get_crud)):
    characters = get_characters_from_db(crud=crud)
    return [CharacterInfo.from_orm(character) for character in characters]


@router.post("")
def post_character(character_info: CharacterData, crud: CRUD = Depends(get_crud), current_user=Depends(admin_required)):
    
    character_data = character_info.dict()
    add_character_to_db(character_data=character_data, crud=crud)

    return Msg(msg="success")


@router.get("/{character_id}")
def get_character(character_id: int, crud: CRUD = Depends(get_crud)):
    character = get_character_from_db(character_id=character_id, crud=crud)
    return CharacterInfo.from_orm(character)


@router.put("/{character_id}")
def update_character(character_info: CharacterData, character_id: int, crud: CRUD = Depends(get_crud), current_user=Depends(admin_required)):
    character = update_character_from_db(character_id=character_id, character_data=character_info.dict(), crud=crud)
    return CharacterInfo.from_orm(character)


@router.delete("/{character_id}")
def delete_character(character_id: int, crud: CRUD = Depends(get_crud), current_user=Depends(admin_required)):
    character = delete_character_from_db(character_id=character_id, crud=crud)
    return Msg(msg="sucess")


@router.post("/search")
def search_characters(search_info: SearchInfo, crud: CRUD = Depends(get_crud)):
    search_ = search_info.dict()
    characters = get_characters_from_db(crud=crud, skills=search_['skills'], properties=search_['properties'])
    if characters is None:
        raise HTTPException(status_code=404, detail="NO Enemies")
    return [CharacterInfo.from_orm(character) for character in characters]