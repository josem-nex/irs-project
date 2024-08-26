import os
import json

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

game_tag = Table("game_tags", Base.metadata,
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
    Column("game_id", ForeignKey("game.id"), primary_key=True),
)

game_genre = Table("game_genres", Base.metadata,
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
    Column("game_id", ForeignKey("game.id"), primary_key=True),
)

class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    genres = relationship("Genre", secondary="game_genres", back_populates="games")
    tags = relationship("Tag", secondary="game_tags", back_populates="games")

class Genre(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    games = relationship("Game", secondary="game_genres", back_populates="genres")

class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    games = relationship("Game", secondary="game_tags", back_populates="tags")

Base.metadata.create_all(engine)

def populate_database(session: Session, data: list[dict]):
    input_data = [
        Game(title=x.get('title', ''), description=x.get('description', '')) for x in data
    ]
    print([x.title for x in input_data])
    session.add_all(input_data)
    session.commit()

# TODO: improve this as a task probably using a POST endpoint instead of directly populate it
POPULATE = False

if POPULATE:
    with open('scraper-result.json', 'r') as result_json:
        content = ''
        for line in result_json:
            content += line
        data = json.loads(content)
        with Session(bind=engine) as session:
            populate_database(session, data)
    POPULATE = False