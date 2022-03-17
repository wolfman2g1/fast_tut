from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# define the schema for the port requests
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # make this field optional but default to true if missing from req body


""" For sending data to the user"""


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Response(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    id: int
    user_id: int
    owner: UserOut

    class Config:  # tell pydantic to convert the sql model to a dict
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)