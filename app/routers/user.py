from fastapi import status,HTTPException,Depends,Response,APIRouter
from app.database import get_session,Users
from sqlmodel import select,Session
from app.schemas import UserResponse,UserCreate
from email_validator import validate_email, EmailNotValidError
from app.utils import hash_password
from app.Oauth2 import get_current_user


router = APIRouter(
    prefix="/sqlmodel/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    if session.exec(select(Users).where(Users.email == user.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
        
    # Validation is already done by UserCreate (EmailStr), but keeping extra check if needed or remove it. 
    # Since we use EmailStr, explicit validate_email call is redundant but harmless.
    
    hashed_pwd = hash_password(user.password)
    new_user = Users(username=user.username, email=user.email, password=hashed_pwd)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse,status_code=status.HTTP_200_OK)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user