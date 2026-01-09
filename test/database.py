from fastapi.testclient import TestClient
from app.main import app

from app.config import settings
from sqlmodel import  Session, SQLModel, create_engine
from typing import Generator
from app.database import get_session
import pytest
from alembic import command




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
    
 