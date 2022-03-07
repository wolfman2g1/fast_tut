from pydantic import BaseModel, EmailStr
from datetime import datetime


# define the schema for the port requests
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # make this field optional but default to true if missing from req body


""" For sending data to the user"""


class Response(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime
    id: int

    class Config:  # tell pydantic to convert the sql model to a dict
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email : EmailStr
    password: str