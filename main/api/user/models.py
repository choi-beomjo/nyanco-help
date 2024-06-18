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
'''
    @root_validator(pre=True)
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @root_validator(pre=True)
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v
        '''