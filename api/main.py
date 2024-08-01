from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, Game

app = FastAPI()

# TODO: add relationships to the model retrieval
class GameSchema(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/db")
def read_db_data():
    with Session(bind=engine) as session:
        db_games = session.query(Game).all()
        games = [GameSchema.model_validate(x) for x in db_games]

        return [x.json() for x in games]
