
from query.main import Query
from recommendation.graph import *
from query.utils import Utils
import matplotlib.pyplot as plt

if __name__ == "__main__":
    input_query = f"I want to play something action-packed but not set in a medieval theme and has ghosts"
    q = Query(input_query)
    print(q.tokens)
    
    print("-----------------------------")
    
    utils = Utils()
    # print(utils.json_data)

    graph_games = create_graph(utils.json_data)
    
    game = "No Man's Sky"

    
    vecinos_pesados = sorted(graph_games[game].items(), key=lambda item: item[1]["weight"], reverse=True)[:5]

    # Imprime los resultados
    print(f"Los 5 juegos más parecidos a {game} son:")
    for vecino, peso in vecinos_pesados:
        print(f"  {vecino}: {peso['weight']:.2f}")
        
    # print(graph_games.edges(data=True))
    
    
    
    
    
    plt.figure(figsize=(15, 15), frameon=False)  

    pos = nx.spring_layout(graph_games, k=0.8, iterations=20)

    node_sizes = [30 * graph_games.degree[n] for n in graph_games.nodes]

    nx.draw_networkx_nodes(graph_games, pos, node_size=node_sizes, node_color='skyblue', alpha=0.7)
    nx.draw_networkx_edges(graph_games, pos, width=0.2, alpha=0.5)

    threshold = 0.8
    significant_nodes = [node for node in graph_games.nodes if graph_games.degree[node] > threshold]  # Define your threshold
    labels = {node: node for node in significant_nodes}
    nx.draw_networkx_labels(graph_games, pos, labels, font_size=5)

    plt.show()
    