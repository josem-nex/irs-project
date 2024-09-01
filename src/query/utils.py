import json
import os
import sympy
import spacy

nlp = spacy.load("en_core_web_sm")

class Utils:
    """
    A class to extract tags from a JSON file and store them in a list.
    """
    def __init__(self):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.abspath(os.path.join(self.current_path, '..', '..', 'data'))
        self.scraper_path = os.path.abspath(os.path.join(self.data_path, 'scraper_result.json'))
        self.tags_output = os.path.abspath(os.path.join(self.data_path, 'tags.txt'))
        self.genres_output = os.path.abspath(os.path.join(self.data_path, 'genres.txt'))
        self.json_data = self.load_json()
        self.all_tags = self.extract_tags()
        self.all_genres = self.extract_genres()

    def load_json(self):
        with open(self.scraper_path, "r") as f:
            return json.load(f)

    def extract_tags(self):
        """
        Extracts all tags from a JSON file and stores them in a list.   
        or loads the tags from the file if it exists. 
        Args:
          json_data: A list of dictionaries representing the JSON data. 
        Returns:
          A list of all tags.
        """
        if os.path.exists(self.tags_output):
            with open(self.tags_output, "r") as f:
                return [tag.strip().lower() for tag in f.readlines()]
            
        if not self.json_data:
            return Exception("No JSON data found.")
        
            
        all_tags = set()
        for item in self.json_data:
            tags = item.get("tags", [])
            all_tags.update(tags)
            
        self.save_tags(all_tags)
        
        return list(all_tags)
    
    def extract_genres(self):
        """
        Extracts all genres from a JSON file and stores them in a list.   
        or loads the genres from the file if it exists. 
        Args:
          json_data: A list of dictionaries representing the JSON data. 
        Returns:
          A list of all genres.
        """
        if os.path.exists(self.genres_output):
            with open(self.genres_output, "r") as f:
                return [genre.strip().lower() for genre in f.readlines()]
            
        if not self.json_data:
            return Exception("No JSON data found.")
        
        all_genres = set()
        for item in self.json_data:
            genres = item.get("genres", [])
            all_genres.update(genres)
            
        self.save_genres(all_genres)
        
        return list(all_genres)

    def save_tags(self, all_tags):
        with open(self.tags_output, "w") as f:
            for tag in all_tags:
                f.write(tag.lower() + "\n")
    
    def save_genres(self, all_genres):
        with open(self.genres_output, "w") as f:
            for genre in all_genres:
                f.write(genre.lower() + "\n")


def tokenize(query, special_tokens=['and', 'or', 'not', '(', ')', '&', '~', '|']):
    data = nlp(query)
    
    tokens = []
    for token in data:
        if token.text.isalpha() or token.lemma_ in special_tokens:
            if token.lemma_ == "not":
                tokens.append("~")
            elif token.lemma_ == "and":
                tokens.append("&")
            elif token.lemma_ == "or":
                tokens.append("|")
            else:
                tokens.append(token.lemma_)
                
    return tokens

def query_to_dfs(query):
    """
    Transforms a boolean expression into its disjunctive normal form
    
    Args:
    - query : str
        Boolean query.

    Return:
    - instance of class Or
    
    """
    # Tokenize the query
    tokens = tokenize(query)
    
    # Create a string with the tokens
    query = ' '.join(tokens)
    
    # Transform the query into its disjunctive normal form
    query = sympy.to_dnf(query, True)
    
    return query

