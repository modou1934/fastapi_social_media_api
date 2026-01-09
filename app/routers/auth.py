from fastapi import APIRouter,Depends,HTTPException,status,Response
from app.database import get_session
from app.models import Users
from sqlmodel import select,Session
from email_validator import validate_email, EmailNotValidError
from app.utils import hash_password
from app.schemas import UserLogin,Token
from app.utils import verify_password
from app.Oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/login",
    tags=["auth"]
)

@router.post("/",status_code=status.HTTP_200_OK,response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    User = session.exec(select(Users).where(Users.email == user.email)).first()
    if not User:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not verify_password(user.password, User.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    access_token = create_access_token(data={"user_id": User.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

