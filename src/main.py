
from query.main import Query


if __name__ == "__main__":
    input_query = f"Microsoft has offices all over Europe and shooter games are popular in the US."
    q = Query(input_query)
    print(q.tokens)