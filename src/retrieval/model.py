from gensim import corpora, similarities

from ..knowledge.tokenizer import Tokenizer
from ..knowledge.vectorizer import Vectorizer
from ..knowledge.indexing import DataDoc, Indexer

from .transparency import TagTransparentLayer, GenreTransparentLayer
from ..api.utils import get_game

class RetrievalModel:
    def __init__(self, nlp, docs) -> None:
        self.nlp = nlp
        self.tokenizer = Tokenizer(nlp)
        self.is_init = False       

        contents = [x.description for x in docs]

        tokenized_data = self.tokenizer.tokenize(contents, [], [], False, 5)
        data = [DataDoc(docs[i].id, tokenized_data[i]) for i in range(len(docs))]
        self.indexer = Indexer(data)

    def load(self, docs, genres, tags):
        self.genres = genres
        self.tags = tags
        contents = [x.description for x in docs]

        tokenized_data = self.tokenizer.tokenize(contents, [], [], False, 5)
        data = [DataDoc(docs[i].id, tokenized_data[i]) for i in range(len(docs))]

        self.indexer = Indexer(data)
        self.is_init = True

    def add(self, docs):
        contents = [x.description for x in docs]
        tokenized_data = self.tokenizer.tokenize(contents, [], [], False, 5)

        data = [DataDoc(docs[i].id, tokenized_data[i]) for i in range(len(docs))]
        self.indexer.add(data)

    def query(self, query: str, session) -> list:
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
        tokenized_query = self.tokenizer.tokenize(
            [query],
            self.genres,
            self.tags,
            True
        )

        query_genres = []
        query_tags = []

        query_lemmas = [[]]

        for x in tokenized_query[0]:
            if x._.is_genre:
                query_genres.append(x.lemma_)
            if x._.is_tag:
                query_tags.append(x.lemma_)
            query_lemmas[0].append(x.lemma_)

        cost_layers = [
            GenreTransparentLayer(query_genres),
            TagTransparentLayer(query_tags)        
        ]

        _, vectorized_query = Vectorizer.vectorize(
            query_lemmas, 
            True, 
            dictionary=self.indexer.dictionary
        )

        matrix = similarities.MatrixSimilarity( 
            [vector for vector in self.indexer.vectorized_corpus]
        )

        res = matrix[vectorized_query][0]
        res_vect = [(x.id, res[i]) for i, x in enumerate(self.indexer.corpus)]

        result = []

        for x in res_vect:
            if x[1] >= 0.05:
                game = get_game(session, x[0])  

                costs = {
                    "Base": float(x[1])
                }
                total_cost = x[1]          

                for layer in cost_layers:
                    layer_cost = layer.get_cost(game)
                    costs[layer.name()] = layer_cost
                    total_cost += layer_cost

                costs['Total'] = float(total_cost / (len(cost_layers) + 1))

                result.append((x[0], costs))
        # sort by similarity
        result.sort(key=lambda x: x[1]['Total'], reverse=True)
        
        # return the first 10
        return result