from fastapi import APIRouter, Depends, HTTPException
from ..tags import Tags
from db.crud.crud import get_crud, CRUD
from db.model.user import User
from .models import USER


router = APIRouter(tags=[Tags.user])


@router.get("/list")
def get_users(name: str = None, email: str = None, crud: CRUD = Depends(get_crud)):
    filters = {key: value for key, value in (("name", name), ("email", email)) if value}

    db_users = crud.read_all(User, **filters)
    return [{"id": user.id, "name": user.name, "email": user.email} for user in db_users]


@router.get("/{user_id}", response_model=USER)
def get_user(user_id: int, crud: CRUD = Depends(get_crud)):
    db_user = crud.read(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return USER(**db_user.__dict__)


@router.post("/")
def add_user(name: str, email: str, crud: CRUD = Depends(get_crud)):
    db_user = crud.create(User(name=name, email=email))
    return {"id": db_user.id, "name": db_user.name, "email": db_user.email}


@router.delete("/{user_id}")
def delete_user(user_id: int, crud: CRUD = Depends(get_crud)):
    db_user = crud.delete(User, obj_id=user_id)
    return {"response": 200}
