import spacy
from spacy.tokens import Token
from query.tags import Tag



class Query:
    """ 
    A class to represent a query.
    
    Attributes
    ----------
    text : str
        the text of the query
    tokens : list
        the tokens of the query
    entities : list
        the entities of the query
    
    """
    
    def __init__(self, text):
        self.nlp = spacy.load("en_core_web_sm")
        self.tags = Tag().all_tags
        Token.set_extension("is_tag", default=False, force=True)
        self.text = text
        self.tokens = self.tokenize_with_pos(text)
        self.entities = self.extract_entities(text)
        
        
    def __repr__(self):
        return f"Query({self.text})"
        
    def tokenize(self, text):
        doc = self.nlp(text)
        return [token.text for token in doc]
    
    def tokenize_with_pos(self, text):
        doc = self.nlp(text)
        tokens = []
        for token in doc:
            if token.text in self.tags:
                token._.is_tag = True
            tokens.append((token.text, token.pos_, token._.is_tag))
        return tokens
    
    def extract_entities(self, text):
        """ 
        PERSON: People, including fictional ones
        NORP: Nationalities or religious or political groups
        FACILITY: Buildings, airports, highways, bridges, and so on
        ORG: Companies, agencies, institutions, and so on
        GPE: Countries, cities, and states
        LOC: Non GPE locations, mountain ranges, and bodies of water
        PRODUCT: Objects, vehicles, foods, and so on (not services)
        EVENT: Named hurricanes, battles, wars, sports events, and so on
        WORK_OF_ART: Titles of books, songs, and so on
        LAW: Named documents made into laws
        LANGUAGE: Any named language 
        """
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]



