from fastapi.testclient import TestClient
from app.main import app
from app.Oauth2 import create_access_token
from app.config import settings
from sqlmodel import  Session, SQLModel, create_engine,select
from typing import Generator
from app.database import get_session
import pytest
from alembic import command
from app import models




SQLMODEL_DATABASE_URL = f"{settings.DATABASE_URL}_test"
engine = create_engine(SQLMODEL_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)



@pytest.fixture(scope="module")#tutti i fixture con scope module sono eseguiti una volta sola per ogni file che testiamo
def session():
    drop_db_and_tables()            
    create_db_and_tables()
    with Session(engine) as session:
        yield session

@pytest.fixture(scope="module")
def client(session):
    def get_session_override()  -> Generator[Session, None, None]:#faccio override per creare nuovo database copiando quello che avevamo gia
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_session] = get_session_override 
    yield TestClient(app)

@pytest.fixture(scope="module")
def test_user(client):   
    user_data= {"username":"useradmin","email":"cisse@gmail.com","password":"password123"}
    res= client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture(scope="module")
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})


@pytest.fixture(scope="module")
def authorized_client(client,token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture(scope="module")
def test_posts(test_user, session):
    posts_data = [{"title":"1st title","content":"1st content","owner_id":test_user["id"]},
    {"title":"2nd title","content":"2nd content","owner_id":test_user["id"]},
    {"title":"3rd title","content":"3rd content","owner_id":test_user["id"]},
    {"title":"4th title","content":"4th content","owner_id":test_user["id"]},
    {"title":"5th title","content":"5th content","owner_id":test_user["id"]},
    {"title":"6th title","content":"6th content","owner_id":test_user["id"]},
    {"title":"7th title","content":"7th content","owner_id":test_user["id"]}]

    session.add_all(list(map(lambda post: models.Posts(**post),posts_data)))
    session.commit()
    posts= session.exec(select(models.Posts)).all()
    return posts