from spacy import load

nlp = load("en_core_web_sm")
class DataDoc:
    def __init__(self, id, content):
        doc = nlp(content)

        self._id = id
        self._tokens = [token.text for token in doc]

    @property
    def tokens(self):
        return self._tokens
    
    @property
    def id(self):
        return self._id        

class Indexer:
    def __init__(self, data: list[DataDoc]):
        self.corpus = set(data)
        self.invind = InvertedIndex()

        for doc in data:
            # print(doc.tokens)
            self.invind.add(doc)

    def add(self, elements: list[DataDoc]):
        self.corpus = self.corpus.union(set(elements))

        for doc in elements:
            self.invind.add(doc)

    def remove(self, elements: list[DataDoc]):
        self.corpus.difference_update(set(elements))

        for doc in elements:
            self.invind.remove(doc)

    def update(self, elements):
        # TODO
        pass


class InvertedIndex:
    def __init__(self):
        self._tokens = {}

    @property
    def tokens(self) -> dict[str, set]:
        return self._tokens
    
    def add(self, doc: DataDoc):
        for token in doc.tokens:
            if self.tokens.get(token):
                self.tokens[token].add(doc.id)
            else:
                self.tokens[token] = set([doc.id])

    def remove(self, doc: DataDoc):
        for token in doc.tokens:
            if self.tokens.get(token):
                self.tokens[token].remove(doc.id)

    def update(self, old: DataDoc, new: DataDoc):
        old_tok = set(old.tokens)
        new_tok = set(new.tokens)
        intersec = old_tok.intersection(new_tok)

        for token in old_tok.difference(intersec):
            self.tokens[token].remove(old.id)

        for token in new_tok.difference(intersec):
            if self.tokens.get(token):
                self.tokens[token].add(new.id)
            else:
                self.tokens[token] = set([new.id])
    def __str__(self) -> str:
        return str(self.tokens)
