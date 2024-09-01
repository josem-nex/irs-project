from recommendation.Tokenizer import tokenize
def get_tags(game_data: dict , from_file = False):
    if from_file:
        with open("data/tags.txt", "r") as f:
            return [tag.strip() for tag in f.readlines()]
    else:
        tags = set()
        for game in game_data:
            tags.update(game.Tags)
        
        tags_tokenized = tokenize(list(tags))
        tags = []
        for tag in tags_tokenized:
            res = ""
            for token in tag:
                res += token+ " "
            if res != "":
                tags.append(res)
            
        with open("data/tags.txt", "w") as f:
            for tag in tags:
                f.write(tag.lower() + "\n")
        
        return tags
    
def get_genres(game_data: dict, from_file = False):
    if from_file:
        with open("data/genres.txt", "r") as f:
            return [genre.strip() for genre in f.readlines()]
    else:
        genres = set()
        for game in game_data:
            genres.update(game.Genres)
        
        genres_tokenized = tokenize(list(genres))
        genres = []
        for genre in genres_tokenized:
            res = ""
            for token in genre:
                res += token+ " "
            if res != "":
                genres.append(res)
        
        with open("data/genres.txt", "w") as f:
            for genre in genres:
                f.write(genre.lower() + "\n")
        
        return genres