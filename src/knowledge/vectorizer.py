from gensim.corpora import Dictionary
from gensim.models import TfidfModel


class Vectorizer:
    """
    A class that represents a vectorizer.

    Methods
    -------
    vectorize(tokenized_docs, is_query=False, dictionary=None)
        Vectorize the tokenized documents using a TF-IDF model.
        If is_query is True, the function will return the dictionary and the corpus.
    """
    def vectorize(tokenized_docs, is_query=False, dictionary=None):
        # Create a dictionary from the tokenized docs
        if dictionary is None:
            dictionary = Dictionary(tokenized_docs)
        
        # Create a corpus from the tokenized docs
        corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]
        
        if is_query:
            return dictionary, corpus
        
        # Create a TF-IDF model
        tfidf = TfidfModel(corpus)
        vectorized_corpus = tfidf[corpus]
        
        return dictionary, vectorized_corpus
    