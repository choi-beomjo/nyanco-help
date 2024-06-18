from pydantic import BaseModel, Field, root_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
from typing import List, Optional


class User(BaseModel):
    id:     str
    name:   str
    email:  str

    class Config:
        orm_mode = True


class UserInfo(BaseModel):
    name:   Optional[str]
    email:  Optional[str]


class SignUpInfo(BaseModel):
    name: str
    password1: str
    password2: str
    email: EmailStr

    @root_validator(pre=True)
    def not_empty(cls, values):
        for v in values:
            if not v or not v.strip():
                raise ValueError('빈 값은 허용되지 않습니다.')
        return values

    @root_validator(pre=True)
    def passwords_match(cls, values):
        if values.get('password1') != values.get('password2'):
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return values
    

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
        