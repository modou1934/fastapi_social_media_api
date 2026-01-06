import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from app.schemas import TokenData
from app.database import get_session,Users
from sqlmodel import select,Session
from os import getenv
from dotenv import load_dotenv


load_dotenv()



ouath2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    

def verify_access_token(token: str,credentials_exception):
    try:
        decode_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = decode_jwt.get("user_id")
        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token scaduto")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalido")
    return token_data


def get_current_user(token: str = Depends(ouath2_scheme),session: Session = Depends(get_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers= {"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token,credentials_exception)
    user = session.exec(select(Users).where(Users.id == token_data.id)).first()
    return user



