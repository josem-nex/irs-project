
from query.main import Query
from recomendation.graph import *
from query.utils import Utils

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