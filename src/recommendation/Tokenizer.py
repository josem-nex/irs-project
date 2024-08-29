from typing import List, Dict
import spacy

nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"]) 

def tokenize(text: List[str], n_process=1) -> List[str]:
    # process the text with the nlp pipeline, efficiently using multiple processes
    docs = list(nlp.pipe(text, n_process=n_process, batch_size=1000))
    
    # return [[token.lemma_ for token in doc if (token.is_alpha or token.is_digit) and not token.is_punct and (str(token.lemma_) != "game" or str(token.lemma_) !="games")] for doc in docs]
    # return a list of lemmatized tokens, only necessary for the recommendation system
    tokenized_docs = []
    for doc in docs:
        tokens = []
        for token in doc:
            # only take sustantive and adjectives and formas verbales
            if (token.is_alpha or token.is_digit) and not token.is_punct and (token.pos_ == "NOUN" or token.pos_ == "ADJ" or token.pos_ == "VERB"):
                if str(token.lemma_) != "game" and str(token.lemma_) != "games":
                    tokens.append(token.lemma_)
        tokenized_docs.append(tokens)
    return tokenized_docs