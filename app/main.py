from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
import time



app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg.connect(conninfo="host=localhost dbname=fastapi_social_media_api user=postgres password=Smab11Cisse@")
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print(f"Database connection failed: {e}")
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Welcome to NotiClient!"}
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return {"post": posts}

my_post = [{"title": "title of post", "content": "content of post", "id": 1},{"title": "title of post2", "content": "content of post2", "id": 2}]

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post= cursor.fetchone()
    conn.commit()
    return {"new_post":new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return {"post_detail": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return {"post_detail": post}

@app.put("/posts/{id}")
def update_post(id:int , post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURN", (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}