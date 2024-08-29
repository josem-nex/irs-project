from typing import List, Dict
import os
import json

from recommendation.Serializer import load_games
from models.Game import Game
class GameStorage:
    """
    A class to store and manage games.
    
    Attributes
    ----------
    games : List[Game]
        A list of Game objects.
    _scraper_path : str
        The path to the JSON file containing the scraped data.
    
    Methods
    -------
    load_games()
        Load the games from the JSON file.
    
    get_game(title: str) -> Game
        Get a game by title.
    
    get_game_by_index(index: int) -> Game
        Get a game by index.
    
    add_game(game: Game)
        Add a game to the list of games.
    
    remove_game(title: str)
        Remove a game from the list of games.
    """
    def __init__(self):
        self._games: List[Game] = []
        
        data_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data'))
        self._scraper_path = os.path.abspath(os.path.join(data_path, 'scraper_result.json'))
        self._games_data_path = os.path.abspath(os.path.join(data_path, 'games_data.json'))
        self._dictionary_path = os.path.abspath(os.path.join(data_path, 'dictionary.pkl'))
        # print(self._scraper_path)
        
        self.load()

    @property
    def games(self) -> List[Game]:
        return self._games
    
    @property
    def games_data_path(self) -> str:
        return self._games_data_path
    
    def load(self):
        self._games = load_games(self._scraper_path)
                
    def get_game(self, title: str) -> Game:
        for game in self._games:
            if game.Title == title:
                return game
        return None
    
    def get_game_by_index(self, index: int) -> Game:
        return self._games[index]

    def add_game(self, game: Dict):
        self._games.append(Game(
            Title=game.get("Title"),
            Genres=game.get("Genres", []),
            Tags=game.get("Tags", []),
            Description=game.get("Description")
        ))
        
        # Save the game to the JSON file
        with open(self._scraper_path, "w") as f:
            json.dump([g.to_dict() for g in self._games], f, indent=4)
        
    def remove_game(self, title: str):
        for game in self._games:
            if game.Title == title:
                self._games.remove(game)
                break
        
        # Save the game to the JSON file
        with open(self._scraper_path, "w") as f:
            json.dump([g.to_dict() for g in self._games], f, indent=4)
    