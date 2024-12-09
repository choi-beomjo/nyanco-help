# app/api/deps.py

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from db.crud.crud import SessionLocal, CRUD
from db.model.user import User
from api.domain.user.schemas import Token
from core.security import oauth2_scheme, SECRET_KEY, ALGORITHM

from api.domain.user.utils import get_user_by_name

# DB 세션 주입
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_crud(db: Session = Depends(get_db)):
    return CRUD(db)


def get_current_user(token: str = Depends(oauth2_scheme),
                     crud: CRUD = Depends(get_crud)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = get_user_by_name(username, crud=crud)
        return user


