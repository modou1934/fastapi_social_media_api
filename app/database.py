from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select,TIMESTAMP
from typing import Generator
from datetime import datetime
from sqlalchemy import text,Column,DateTime
from urllib.parse import quote_plus

class Posts(SQLModel, table=True):
    id: Optional[int] = Field(nullable=False, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True,sa_column_kwargs={"server_default": "true"} )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=text("NOW()"),
            nullable=False
        )
    )


db_password = quote_plus("Smab11Cisse@")
SQLMODEL_DATABASE_URL = f"postgresql://postgres:{db_password}@localhost:5432/fastapi_social_media_api"
engine = create_engine(SQLMODEL_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session()  -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

'''@app.post("/hero", status_code=status.HTTP_201_CREATED, response_model=Hero)
def create_hero(hero: Hero, session: Session = Depends(get_session)):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/hero", response_model=list[Hero])
def read_heroes(session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes

@app.get("/hero/{hero_id}", response_model=Hero)
def read_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    return hero

@app.delete("/hero/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return None

@app.put("/hero/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero_update: Hero, session: Session = Depends(get_session)):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")

    db_hero.title = hero_update.title
    db_hero.content = hero_update.content
    db_hero.published = hero_update.published

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
'''