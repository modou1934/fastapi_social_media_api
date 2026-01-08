from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import post,user,auth,like
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
#create_db_and_tables() 

origins =["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)
@app.get("/")
def root():
    return {"message": "Welcome to NotiClient!!!!!"}




























