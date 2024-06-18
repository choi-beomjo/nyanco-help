from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette import status
from datetime import datetime, timedelta
from typing import List
from ..tags import Tags
from db.crud.crud import get_crud, CRUD
from .utils import *
from .models import *
from utils.msg.msg import Msg

router = APIRouter(tags=[Tags.user])

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"


@router.post("/search", response_model=List[User])
def get_users(user_info: UserInfo, crud: CRUD = Depends(get_crud)):
    db_users = get_users_from_db(user_info=user_info, crud=crud)
    return [User.from_orm(user) for user in db_users]


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, crud: CRUD = Depends(get_crud)):
    db_user = get_user_from_db(user_id=user_id, crud=crud)
    return User.from_orm(db_user)


@router.post("/signup", response_model=User)
def add_user(user_info: SignUpInfo, crud: CRUD = Depends(get_crud)):
    check_user_existed(user_info=user_info, crud=crud)

    db_user = add_user_to_db(user_info=user_info, crud=crud)
    return User.from_orm(db_user)


@router.delete("/{user_id}", response_model=Msg)
def delete_user(user_id: int, crud: CRUD = Depends(get_crud)):
    delete_user_from_db(user_id=user_id, crud=crud)
    return Msg(msg="success")


@router.post('/login')
def user_login(form_data: OAuth2PasswordRequestForm = Depends(),
               crud: CRUD = Depends(get_crud)):
    user = get_user_by_name(form_data.username, crud)
    
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    data = {
        "sub": user.name,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.name
    }