from typing import List
from gensim import corpora, similarities

from recommendation.GameStorage import GameStorage
from models.Game import Game
from models.GameData import GameData
from models.GameOut import GameOut
from recommendation.Tokenizer import tokenize
from recommendation.Vectorizer import vectorize
from recommendation.Serializer import load_games_data, save_json


class RecSystem:
    """
    A class to recommend games based on user input.
    """
    def __init__(self, is_from_file: bool = False):
        self.game_storage: GameStorage = GameStorage()
        self.games_data: List[GameData] = []
        self.dictionary: corpora.Dictionary = None 
        
        self.load()
        
    
    def load(self, is_from_file: bool = False):
        if is_from_file:
            self.games_data = load_games_data(self.game_storage.games_data_path)
            self.dictionary = corpora.Dictionary.load(self.game_storage.dictionary_path)
        else:
                        
            texts = [game.Description for game in self.game_storage.games]
            
            tokenized_corpus = tokenize(texts, 4)
            
            self.dictionary, vectorized_corpus = vectorize(tokenized_corpus)
                        
            for game, vector in zip(self.game_storage.games, vectorized_corpus):
                self.games_data.append(GameData(
                    Title=game.Title,
                    Genres=game.Genres,
                    Tags=game.Tags,
                    Description=game.Description,
                    Vector=vector
                ))
                
            save_json(self.games_data, self.game_storage._games_data_path)
            self.dictionary.save(self.game_storage._dictionary_path)
            
    def add_game(self, game: Game):
        self.game_storage.add_game(game)
        self.load()
        
    def query(self, query: str) -> List[GameOut]:
        """
        Query the system for game recommendations.
        
        Parameters
        ----------
        query : str
            The user query.
        
        Returns
        -------
        List[GameOut]
            A list of GameOut objects.
        """
        tokenized_query = tokenize([query])
        
        _, vectorized_query = vectorize(tokenized_query, True, dictionary=self.dictionary)
        
        matrix = similarities.MatrixSimilarity( 
            [game.Vector for game in self.games_data]
        )
        # print(vectorized_query)
        
        res = matrix[vectorized_query][0]
        
        game_vec = [GameOut(
            Title=self.games_data[i].Title,
            Genres=self.games_data[i].Genres,
            Tags=self.games_data[i].Tags,
            Description=self.games_data[i].Description,
            Similarity=res[i]
        ) for i in range(len(res))]
        
        # sort by similarity
        game_vec.sort(key=lambda x: x.Similarity, reverse=True)
        
        # return the first 10
        return game_vec[:10]