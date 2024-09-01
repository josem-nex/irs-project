from spacy import load
from typing import Union

from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import engine, Game, Genre, Tag
from .logic import get_results_from_query
from .serializers import GameSchema, TagSchema, GenreSchema
from ..recommendation.RecSystem import RecSystem
from ..recommendation.model import RetrievalModel



# rec = RecSystem(True)
nlp = load("en_core_web_sm", disable=["ner", "parser"]) 
rec = RetrievalModel(nlp, [])

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if not rec.is_init:
        with Session(bind=engine) as session:
            db_games = session.query(Game).all()
            db_genres = session.query(Genre).all()
            db_tags = session.query(Tag).all()

        games = [GameSchema.model_validate(x) for x in db_games]
        genres = [GenreSchema.model_validate(x).name.lower() for x in db_genres]
        tags = [TagSchema.model_validate(x).name.lower() for x in db_tags]
        rec.load([], genres, tags)

        chunk_size = 200
        for i in range(int(len(games)/chunk_size)):
            rec.add(games[i*chunk_size:(i+1)*chunk_size])
    
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/query/")
# def process_query(results = Depends(get_results_from_query)):
def process_query(q: str):
    with Session(bind=engine) as session:
        res = rec.query(q, session)
        ret = []
        for x in res:
            data = GameSchema.model_validate(
                session.query(Game).filter(Game.id == x[0]).one()
            )

            ret.append({
                'title': data.title,
                'description': data.description[:300]+"...",
                'image': data.image,
                'genres': [x.name for x in data.genres],
                'tags': [x.name for x in data.tags],
                'values': x[1]
            }) 
        return ret

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/test")
def test_req():
    return {"hello": "world"}

@app.get("/db")
def read_db_data():
    with Session(bind=engine) as session:
        db_games = session.query(Game).all()
        games = [GameSchema.model_validate(x) for x in db_games]

        return [x.json() for x in games]
