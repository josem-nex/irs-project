from recommendation.GameStorage import GameStorage
from recommendation.RecSystem import RecSystem
def test_game_storage():
    
    rec = RecSystem()
    res = rec.query("A game about fighting dragons")
    
    for r in res:
        print(r.Title)
    pass    

test_game_storage()