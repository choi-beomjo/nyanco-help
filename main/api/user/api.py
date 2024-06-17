from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..tags import Tags
from db.crud.crud import get_crud, CRUD
from db.model.user import User
from .models import USER, UserInfo
from .utils import *


router = APIRouter(tags=[Tags.user])


@router.post("/search", response_model=List[USER])
def get_users(user_info: UserInfo, crud: CRUD = Depends(get_crud)):
    db_users = get_users_from_db(user_info=user_info, crud=crud)
    return [USER(**user.__dict__) for user in db_users]


@router.get("/{user_id}", response_model=USER)
def get_user(user_id: int, crud: CRUD = Depends(get_crud)):
    db_user = get_user_from_db(user_id=user_id, crud=crud)
    return USER(**db_user.__dict__)


@router.post("/")
def add_user(user_info: UserInfo, crud: CRUD = Depends(get_crud)):
    db_user = crud.create(User(**user_info.dict()))
    return {"id": db_user.id, "name": db_user.name, "email": db_user.email}


@router.delete("/{user_id}")
def delete_user(user_id: int, crud: CRUD = Depends(get_crud)):
    db_user = crud.delete(User, obj_id=user_id)
    return {"response": 200}
