import networkx as nx

def create_graph(games):
    """
    Creates a graph of games based on genres and tags.

    Args:
      games: A list of dictionaries with game information.

    Returns:
      A NetworkX graph object.
    """
    
    graph = nx.Graph()
    
    for i, gamei in enumerate(games):
        
        graph.add_node(gamei["title"])
        
        for j in range(i+1, len(games)):
            
            gamej = games[j]
            
            genre_cost = calculate_genre_cost(gamei,gamej)
            tag_cost = calculate_tag_cost(gamei,gamej)
            total_cost = (genre_cost*0.5) + (tag_cost*0.3)
            
            if total_cost >0.4:
                graph.add_edge(gamei["title"], gamej["title"],weight=total_cost)
    
    return graph

def calculate_genre_cost(gamei,gamej):
    """
    Calculates the cost of the edge based on shared genres.

    Args:
      gamei: A dictionary with information about a game.
      gamej: A dictionary with information about another game.

    Returns:
      The cost of the edge (0 <= cost <= 1).
    """

    shared_genres = set(gamei["genres"]) & set(gamej["genres"])
    
    return len(shared_genres) / len(set(gamei["genres"]) | set(gamej["genres"]))

def calculate_tag_cost(gamei,gamej):
    """
    Calculates the cost of the edge based on shared tags.

    Args:
      gamei: A dictionary with information about a game.
      gamej: A dictionary with information about another game.

    Returns:
      The cost of the edge (0 <= cost <= 1).
    """

    shared_tags = set(gamei["tags"]) & set(gamej["tags"])
    return len(shared_tags) / len(set(gamei["tags"]) | set(gamej["tags"]))