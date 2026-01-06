from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select,Relationship
from typing import Generator
from datetime import datetime
from sqlalchemy import text,Column,DateTime,Integer,ForeignKey
from urllib.parse import quote_plus

class Users(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False,primary_key=True)
    username: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, unique=True, index=True) 
    password: str = Field(nullable=False)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("NOW()"), 
            nullable=False
        )
    )
    posts: list["Posts"] = Relationship(back_populates="owner")

class Posts(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True,sa_column_kwargs={"server_default": "true"} )
    owner_id: Optional[int] = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("NOW()"),
            nullable=False
        )
    )
    owner: Users = Relationship(back_populates="posts")

db_password = quote_plus("Smab11Cisse@")    
SQLMODEL_DATABASE_URL = f"postgresql://postgres:{db_password}@localhost:5432/fastapi_social_media_api"
engine = create_engine(SQLMODEL_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session()  -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

