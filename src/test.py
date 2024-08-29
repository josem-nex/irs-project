from recommendation.GameStorage import GameStorage
from recommendation.RecSystem import RecSystem
def test_game_storage():
    
    rec = RecSystem(True)
    res = rec.query("A game about fighting dragons")
    
    for r in res:
        print(r.Title)
        print(r.Similarity)
    pass    

test_game_storage()