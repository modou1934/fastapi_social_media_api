from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg
import time
from .database import get_session,create_db_and_tables,Posts,Users
from sqlmodel import SQLModel,select,Session
from fastapi import Depends
from .schemas import Post,PostResponse,User,UserResponse
from email_validator import validate_email, EmailNotValidError
from .utils import hash_password
from .routers import post,user
from .routers import auth





app = FastAPI()

create_db_and_tables() 
    


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get("/")
def root():
    return {"message": "Welcome to NotiClient!"}




























