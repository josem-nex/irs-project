
from query.main import Query


if __name__ == "__main__":
    input_query = f"I want to play something action-packed but not set in a medieval theme and has ghosts"
    q = Query(input_query)
    print(q.tokens)