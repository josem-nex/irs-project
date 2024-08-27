from spacy import load
import sympy
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
        self._titles = set()

    @property
    def tokens(self) -> dict[str, set]:
        return self._tokens
    
    def add(self, doc: DataDoc):
        self._titles.add(doc.id)
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
    def matching_docs(self, query_dnf):
        """Finds the documents that match the query in disjunctive normal form.
    
        Args:
            query_dnf : Instance of class Or
                Disjunctive normal form of a query.
        
        Returns:
            set : Set of documents that match the query.
        """
        # Initialize the set of documents that match the query
        matching_docs = set()
        
        # Iterate over the terms of the query
        if query_dnf.func == sympy.Or:
            for term in query_dnf.args:
                # Initialize the set of documents that match the term
                term_docs = None
                
                # Iterate over the literals of the term
                for literal in term.args:
                    # Check if the literal is a negation
                    if literal.func == sympy.Not:
                        # Get the documents that do not match the literal
                        docs = self.tokens.get(str(literal.args[0]), set())
                        if term_docs is None:
                            term_docs = set(self._titles) - docs
                        else:
                            term_docs &= set(self._titles) - docs
                    else:
                        # Get the documents that match the literal
                        docs = self.tokens.get(str(literal), set())
                        if term_docs is None:
                            term_docs = docs
                        else:
                            term_docs &= docs
                
                # Update the set of documents that match the query
                if term_docs:
                    matching_docs |= term_docs
            
            return matching_docs
        else:
            term_docs = None
            term = query_dnf
            # Iterate over the literals of the term
            for literal in term.args:
                # Check if the literal is a negation
                if literal.func == sympy.Not:
                    # Get the documents that do not match the literal
                    docs = self.tokens.get(str(literal.args[0]), set())
                    if term_docs is None:
                        term_docs = set(self._titles) - docs
                    else:
                        term_docs &= set(self._titles) - docs
                else:
                    # Get the documents that match the literal
                    docs = self.tokens.get(str(literal), set())
                    if term_docs is None:
                        term_docs = docs
                    else:
                        term_docs &= docs
            
            # Update the set of documents that match the query
            if term_docs:
                matching_docs |= term_docs
            return matching_docs
    
    def __str__(self) -> str:
        return str(self.tokens)
