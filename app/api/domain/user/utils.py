from fastapi import HTTPException
from passlib.context import CryptContext
from .models import User
from db.crud.crud import CRUD

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_from_db(user_id: int, crud: CRUD):
    db_user = crud.read(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_users_from_db(user_info, crud: CRUD):
    filters = {key: value for key, value in user_info if value}
    db_users = crud.read_all(User, **filters)
    return db_users


def add_user_to_db(user_info: User, crud: CRUD):
    return crud.create(User(name=user_info.name, 
                            email=user_info.email, 
                            password=pwd_context.hash(user_info.password1)))


def delete_user_from_db(user_id: int, crud: CRUD):
    db_user = crud.delete(User, obj_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    

def check_user_existed(user_info, crud: CRUD):
    filters = {"email": user_info.email}
    existing_user = crud.read_all(User, **filters)
    if len(existing_user) > 0:
        raise HTTPException(status_code=400, detail="Already existing email")
    

def get_user_by_name(name, crud: CRUD):
    users = crud.read_all(model=User, name=name)
    if len(users) < 1:
        raise HTTPException(status_code=400, detail=f"There is no username ({name}))")
    return users[0]
