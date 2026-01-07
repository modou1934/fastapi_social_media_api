from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select,Relationship
from datetime import datetime
from sqlalchemy import text,Column,DateTime,Integer,ForeignKey




class Users(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False,primary_key=True)
    username: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, unique=True, index=True) 
    password: str = Field(nullable=False)
    phone_number: int = Field(nullable=True)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("NOW()"), 
            nullable=False
        )
    )
    posts: list["Posts"] = Relationship(back_populates="owner")
    likes: list["Likes"] = Relationship(back_populates="user")

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
    likes: list["Likes"] = Relationship(back_populates="post")


class Likes(SQLModel, table=True):
    user_id: Optional[int] = Field(sa_column=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False,primary_key=True))
    post_id: Optional[int] = Field(sa_column=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False,primary_key=True))
    user: Users = Relationship(back_populates="likes")
    post: Posts = Relationship(back_populates="likes")