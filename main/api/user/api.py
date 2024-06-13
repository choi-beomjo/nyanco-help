from fastapi import APIRouter, Depends, HTTPException
from ..tags import Tags
from db.crud.crud import get_crud, CRUD
from db.model.user import User


router = APIRouter()
tag = Tags.user

@router.get("/{user_id}", tags=[tag])
def get_user(user_id: int, crud: CRUD = Depends(get_crud)):
    db_user = crud.read(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": db_user.id, "name": db_user.name, "email": db_user.email}


@router.post("/", tags=[tag])
def add_user(name: str, email: str, crud: CRUD = Depends(get_crud)):
    db_user = crud.create(User(name=name, email=email))
    return {"id": db_user.id, "name": db_user.name, "email": db_user.email}