from fastapi import APIRouter, Depends, Body, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from starlette import status
from datetime import datetime, timedelta
from typing import List
from ...tags import Tags
from ...deps import get_current_user, get_crud, CRUD, get_redis
from .utils import *
from .schemas import *
from utils.msg.msg import Msg
from core.security import *
import redis.asyncio as redis
import secrets


router = APIRouter(tags=[Tags.user])


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
async def user_login(
            response: Response,
            form_data: OAuth2PasswordRequestForm = Depends(),
               crud: CRUD = Depends(get_crud),
               redis: redis.Redis = Depends(get_redis)):
    
    user = get_user_by_name(form_data.username, crud)
    
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": user.name,
        "exp": int(expire.timestamp())
    }

    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    refresh_token = secrets.token_urlsafe(32)

    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

    await redis.set(f"refresh_token:{user.name}", refresh_token, ex=REFRESH_TOKEN_EXPIRE_MINUTES * 60)
    await redis.set(f"refresh_token:{refresh_token}", user.name, ex=REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    response.set_cookie(key="refresh_token", 
                        value=refresh_token, 
                        httponly=True, 
                        secure=False, 
                        samesite="lax",
                        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
                        path="/api/user/token/refresh")
    
    return JSONResponse(status_code=200, content={
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    },
    headers=response.headers)


@router.post('/token/refresh')
async def refresh_token_endpoint(request: Request,
                           redis: redis.Redis = Depends(get_redis)):

    try:
        refresh_token = request.cookies.get("refresh_token")
    except AttributeError:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    
    username = await redis.get(f"refresh_token:{refresh_token}")

    saved_token = await redis.get(f"refresh_token:{username}")
    
    if saved_token != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 새 access token 발급
    new_access = jwt.encode({
        "sub": username,
        "exp": int(expire.timestamp())
    }, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": new_access,
        "token_type": "bearer"
    }


@router.post('/token/logout')
async def logout_token(request: Request, response: Response,
                access_token: str = Depends(oauth2_scheme),
                redis: redis.Redis = Depends(get_redis)):
    
    if not access_token:
        raise HTTPException(401, "No access token")

    # access_token 블랙리스트에 추가 (만료 시간까지 저장)
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        exp = payload.get("exp")
        ttl = exp - int(datetime.utcnow().timestamp())
        await redis.setex(f"blacklist:{access_token}", ttl, "logout")
    except JWTError:
        raise HTTPException(401, "Invalid access token")

    # refresh_token 제거
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await redis.delete(f"refresh_token:{refresh_token}")

    # 쿠키 삭제
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie(key="refresh_token", path="/api/user/token/refresh")

    return response