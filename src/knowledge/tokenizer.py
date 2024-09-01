import spacy
from typing import List

class Tokenizer:
    """
    A class to tokenize text using the spacy pipeline.

    Attributes
    ----------
    nlp : spacy.lang.en.English
        The English language model.

    Methods
    -------
    tokenize(text: List[str], genres=[], tags=[], is_query=False, n_process=1) -> List[str]
        Tokenize the text using the spacy pipeline.
        If is_query is True, the function will also tag the tokens that are genres or tags.
    
    """
    def __init__(self, nlp) -> None:
        self.nlp = nlp
        spacy.tokens.Token.set_extension("is_tag", default=False, force=True)
        spacy.tokens.Token.set_extension("is_genre", default=False, force=True)

    def tokenize(self, text: List[str], genres=[], tags=[], is_query=False, n_process=1) -> List[str]:
    # process the text with the nlp pipeline, efficiently using multiple processes
        docs = list(self.nlp.pipe(text, n_process=n_process, batch_size=1000))
        
        tokenized_docs = []
        if is_query:
            for doc in docs:
                tokens = []
                for token in doc:
                    # only take sustantive and adjectives and formas verbales
                    if (token.lemma_ in tags):
                        token._.is_tag = True
                    if (token.lemma_ in genres):
                        token._.is_genre = True
                    if (token.is_alpha or token.is_digit) and not token.is_punct and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "VERB"):
                        if str(token.lemma_) != "game" and str(token.lemma_) != "games":
                            tokens.append(token)
                tokenized_docs.append(tokens)
            return tokenized_docs
        tokenized_docs = []
        for doc in docs:
            tokens = []
            for token in doc:
                if (token.is_alpha or token.is_digit) and not token.is_punct and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "VERB"):
                    if str(token.lemma_) != "game" and str(token.lemma_) != "games":
                        tokens.append(token.lemma_)
            tokenized_docs.append(tokens)
        return tokenized_docs
    