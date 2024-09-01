from sqlalchemy.orm import joinedload

from .database import Game, Tag, Genre
from .serializers import GameSchema

def get_game(session, game_id):
    res = session.query(Game).options(
        joinedload(Game.genres)
    ).filter(Game.id == game_id).one()
    game = GameSchema.model_validate(
        res
    )

    return game
