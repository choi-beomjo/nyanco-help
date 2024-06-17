from fastapi import APIRouter, Depends
from typing import List
from ..tags import Tags
from db.crud.crud import get_crud, CRUD
from .utils import *
from .models import *

router = APIRouter(tags=[Tags.user])


@router.post("/search", response_model=List[User])
def get_users(user_info: UserInfo, crud: CRUD = Depends(get_crud)):
    db_users = get_users_from_db(user_info=user_info, crud=crud)
    return [User.from_orm(user) for user in db_users]


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, crud: CRUD = Depends(get_crud)):
    db_user = get_user_from_db(user_id=user_id, crud=crud)
    return User.from_orm(db_user)


@router.post("/")
def add_user(user_info: UserInfo, crud: CRUD = Depends(get_crud)):
    db_user = add_user_to_db(user_info=user_info, crud=crud)
    return User.from_orm(db_user)


@router.delete("/{user_id}")
def delete_user(user_id: int, crud: CRUD = Depends(get_crud)):
    delete_user_from_db(user_id=user_id, crud=crud)
    return {"response": 200}
