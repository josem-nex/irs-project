from pydantic import BaseModel


class TagSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class GameSchema(BaseModel):
    id: int
    title: str
    description: str
    tags: list[TagSchema]
    genres: list[GenreSchema]
    image: str

    class Config:
        from_attributes = True
