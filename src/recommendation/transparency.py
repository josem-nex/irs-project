class TransparentLayer:
    """
        This class defines a simple way to represent transparency to provide 
        the user with a feedback of how the data was processed.
        The core idea behind is to have a set of parameters, and a cost function for a 
        given item provided, then with the description function we debscribe the way this 
        cost function works, in a way the user can understand.
    """
    def params(self):
        """
            The params provided to the layer for the cost calculation.
        """
        return []
    
    def description(self):
        """
            User readable string debscribing how the layer works.
        """
        return ""
    
    def get_cost(self, item):
        """
            Cost function that given an item (some result from the search span retrieved by the 
            Information Retrieval model used) it returns a cost.
        """
        return 0
    
class TagTransparentLayer(TransparentLayer):
    def __init__(self, tags):
        self.tags = tags

    def params(self):
        return self.tags
    
    def description(self):
        return f"We used game tags extracted from the query \
            to process the results. The tags used were {self.params}"
    
class GenreTransparentLayer(TransparentLayer):
    def __init__(self, genres):
        self.genres = genres

    def params(self):
        return self.genres
    
    def description(self):
        return f"We used genre keywords extracted from the query \
            to process the results. The genres used were {self.params}"
    