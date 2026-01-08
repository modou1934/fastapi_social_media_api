from fastapi import status,HTTPException,Depends,Response,APIRouter
from app.database import get_session
from app.models import Posts,Users,Likes
from sqlmodel import select,Session
from app.schemas import UserResponse,UserCreate,Like
from email_validator import validate_email, EmailNotValidError
from app.utils import hash_password
from app.Oauth2 import get_current_user


router = APIRouter(
    prefix="/likes",
    tags=["likes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_like(like: Like, session: Session = Depends(get_session),current_user: Users = Depends(get_current_user)):
    if not session.get(Posts,like.post_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post = session.exec(select(Likes).where(Likes.post_id == like.post_id, Likes.user_id == current_user.id)).first()
    if like.dir == 1:
        if post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post already liked")
        session.add(Likes(post_id = like.post_id, user_id= current_user.id))
        session.commit()
        return {"like":"like successfully added!!"}
    else:
        if not post:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post not found")
        session.delete(post)
        session.commit()
        return {"like":"like successfully removed!!"}
   
