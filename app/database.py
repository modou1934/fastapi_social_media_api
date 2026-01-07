from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select,Relationship
from typing import Generator
from datetime import datetime
from sqlalchemy import text,Column,DateTime,Integer,ForeignKey
from app.config import settings





SQLMODEL_DATABASE_URL = f"postgresql://{settings.my_db_user}:{settings.my_db_password}@{settings.my_db_host}:{settings.my_db_port}/{settings.my_db_name}"
engine = create_engine(SQLMODEL_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session()  -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

