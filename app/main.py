from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Welcome to NotiClient!"}
@app.get("/posts")
def get_posts():
    return {"post": my_post}

my_post = [{"title": "title of post", "content": "content of post", "id": 1},{"title": "title of post2", "content": "content of post2", "id": 2}]
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    return {"new_post":post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post =[post for post in my_post if post['id'] == id]
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return {"post_detail": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for n,post in enumerate(my_post):
        if post['id'] == id:
            my_post.pop(n)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

@app.put("/posts/{id}")
def update_post(id:int , post: Post):
    for n,p in enumerate(my_post):
        if p['id'] == id:
            post_dict = post.dict()
            post_dict['id'] = id
            my_post[n] = post_dict
            return {"data": post_dict}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")