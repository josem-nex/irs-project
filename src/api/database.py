import os
import json

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

POPULATE = not os.path.exists("./sql_app.db")

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
    image = Column(String)
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
    for x in data:
        input_data = []
        game = Game(
            title=x.get('title', ''), 
            description=x.get('description', ''),
            image=x.get('image')
        )
        for genre in x.get('genres', []):
            try:
                db_genre = session.query(Genre).filter(Genre.name == genre).one()
            except:
                db_genre = Genre(name=genre)
                input_data.append(db_genre)
            finally:
                game.genres.append(db_genre)
        for tag in x.get('tags', []):
            try:
                db_tag = session.query(Tag).filter(Tag.name == tag).one()
            except:
                db_tag = Tag(name=tag)
                input_data.append(db_tag)
            finally:
                game.tags.append(db_tag)
        input_data.append(game)
        session.add_all(input_data)
        session.commit()

# TODO: improve this as a task probably using a POST endpoint instead of directly populate it

if POPULATE:
    with open('scraper-result.json', 'r') as result_json:
        with Session(bind=engine) as session:
            # content = ''
            # for line in result_json:
            #     content += line
            data = json.load(result_json)
            populate_database(session, data)
    POPULATE = False