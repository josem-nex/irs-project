from ..query.main import Query

rec = None

def get_results_from_query(q: str):
    
    query = Query(q)

    # print(query.tokens)

    return query.tokens

