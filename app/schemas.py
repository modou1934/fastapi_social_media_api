from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True



class User(BaseModel):
    username: Optional[str] = None
    email: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(User):
    id: int
    created_at: datetime

class PostResponse(Post):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserResponse

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
