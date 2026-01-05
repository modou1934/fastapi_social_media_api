from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)

# Use psycopg (psycopg3) driver. Install with `pip install psycopg[binary]` or install `psycopg2` if preferred.
SQLMODEL_DATABASE_URL = 'postgresql+psycopg://postgres:Smab11Cisse@localhost:5432/fastapi_social_media_api'
engine = create_engine(SQLMODEL_DATABASE_URL)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session


