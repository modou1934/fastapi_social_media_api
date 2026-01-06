from fastapi import status,HTTPException,Depends,Response,APIRouter
from typing import Optional
from app.database import get_session,Posts,Users
from sqlmodel import select,Session
from app.schemas import Post,PostResponse
import time
import psycopg
from app.Oauth2 import get_current_user



router = APIRouter(
    prefix="/sqlmodel/posts",
    tags=["posts"]
)
## SQLMODEL
@router.get("/", response_model=list[PostResponse],status_code=status.HTTP_200_OK)  
def read_posts(session: Session = Depends(get_session),limit: int = 10, skip: int = 0,search: Optional[str] = None):
    posts = session.exec(select(Posts).limit(limit).offset(skip).where(Posts.title.contains(search))).all()
    return posts  

@router.post("/", response_model=PostResponse,status_code=status.HTTP_201_CREATED)
def create_post(post: Posts, session: Session = Depends(get_session),current_user: Users = Depends(get_current_user)):
    post.owner_id = current_user.id
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


@router.get("/{post_id}", response_model=PostResponse,status_code=status.HTTP_200_OK)
def read_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Posts, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session),current_user: Users = Depends(get_current_user)):
    post = session.get(Posts, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    session.delete(post)
    session.commit()
    return None

@router.put("/{post_id}", response_model=PostResponse,status_code=status.HTTP_200_OK)
def update_post(post_id: int, post: Posts, session: Session = Depends(get_session),current_user: Users = Depends(get_current_user)):
    db_post = session.get(Posts, post_id)
    
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db_post.title = post.title
    db_post.content = post.content
    db_post.published = post.published
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post





'''## RAW SQL
while True:
    try:
        conn = psycopg.connect(conninfo="host=localhost dbname=fastapi_social_media_api user=postgres password=Smab11Cisse@")
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print(f"Database connection failed: {e}")
        time.sleep(2)

@router.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    print(posts)
    return posts

my_post = [{"title": "title of post", "content": "content of post", "id": 1},{"title": "title of post2", "content": "content of post2", "id": 2}]

@router.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post= cursor.fetchone()
    conn.commit()
    return new_post

@router.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post


@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s", (id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post

@router.put("/posts/{id}")
def update_post(id:int , post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURN", (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return post'''