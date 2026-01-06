from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import post,user,auth
from .config import settings


app = FastAPI()
create_db_and_tables() 

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
@app.get("/")
def root():
    return {"message": "Welcome to NotiClient!"}




























