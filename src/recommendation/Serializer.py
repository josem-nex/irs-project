import json
from typing import List, Dict

from models.Game import Game
from models.GameData import GameData


def load_json(file_path: str) -> Dict:
    """
    Load JSON data from a file.
    
    Parameters
    ----------
    file_path : str
        The path to the JSON file.
    
    Returns
    -------
    Dict
        The JSON data.
    """
    with open(file_path, "r") as f:
        return json.load(f)

def load_games(file_path: str) -> List[Game]:
    """
    Load games from a JSON file.
    
    Parameters
    ----------
    file_path : str
        The path to the JSON file.
    
    Returns
    -------
    List[Game]
        A list of Game objects.
    """
    json_data = load_json(file_path)
    games = []
    for item in json_data:
        games.append(Game(
            Title=item.get("Title"),
            Description=item.get("Description"),
            Genres=item.get("Genres", []),
            Tags=item.get("Tags", [])
        ))
    return games

def load_games_data(file_path: str) -> List[GameData]:
    """
    Load games data from a JSON file.
    
    Parameters
    ----------
    file_path : str
        The path to the JSON file.
    
    Returns
    -------
    List[GameData]
        A list of GameData objects.
    """
    json_data = load_json(file_path)
    games_data = []
    for item in json_data:
        games_data.append(GameData(
            Title=item.get("Title"),
            Genres=item.get("Genres", []),
            Tags=item.get("Tags", []),
            Description=item.get("Description"),
            Vector=item.get("Vector", [])
        ))
    return games_data

def save_json(games: List[Game], file_path: str):
    """
    Save games to a JSON file.
    
    Parameters
    ----------
    games : List[Game]
        A list of Game objects.
    file_path : str
        The path to the JSON file.
    """
    with open(file_path, "w") as f:
        json.dump([g.to_dict() for g in games], f, indent=4)