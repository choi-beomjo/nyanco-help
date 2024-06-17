from fastapi import HTTPException
from db.model.user import User
from db.crud.crud import CRUD


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
    return crud.create(User(**user_info.dict()))


def delete_user_from_db(user_id: int, crud: CRUD):
    db_user = crud.delete(User, obj_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")