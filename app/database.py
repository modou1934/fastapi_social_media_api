from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select,Relationship
from typing import Generator
from datetime import datetime
from sqlalchemy import text,Column,DateTime,Integer,ForeignKey
from app.config import settings





SQLMODEL_DATABASE_URL = f"{settings.my_db_url}"
engine = create_engine(SQLMODEL_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session()  -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

