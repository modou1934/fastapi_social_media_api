from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg
import time
from .database import get_session,create_db_and_tables,Posts
from sqlmodel import SQLModel,select,Session
from fastapi import Depends
from .schemas import Post



app = FastAPI()

create_db_and_tables() 
    
while True:
    try:
        conn = psycopg.connect(conninfo="host=localhost dbname=fastapi_social_media_api user=postgres password=Smab11Cisse@")
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print(f"Database connection failed: {e}")
        time.sleep(2)

## SQLMODEL
@app.get("/sqlmodel/posts", response_model=list[Posts])  
def read_posts(session: Session = Depends(get_session)):
    posts = session.exec(select(Posts)).all()
    return posts  

@app.post("/sqlmodel/posts", response_model=Posts)
def create_post(post: Posts, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@app.get("/sqlmodel/posts/{post_id}", response_model=Posts)
def read_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Posts, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@app.delete("/sqlmodel/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Posts, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    session.delete(post)
    session.commit()
    return None

@app.put("/sqlmodel/posts/{post_id}", response_model=Posts)
def update_post(post_id: int, post: Posts, session: Session = Depends(get_session)):
    db_post = session.get(Posts, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post



## RAW SQL

@app.get("/")
def root():
    return {"message": "Welcome to NotiClient!"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return posts

my_post = [{"title": "title of post", "content": "content of post", "id": 1},{"title": "title of post2", "content": "content of post2", "id": 2}]

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post= cursor.fetchone()
    conn.commit()
    return new_post

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post

@app.put("/posts/{id}")
def update_post(id:int , post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURN", (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post