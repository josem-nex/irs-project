from dataclasses import dataclass, field
from typing import List

@dataclass
class GameData:
    Title: str
    Description: str
    Genres: List[str] = field(default_factory=list)
    Tags: List[str] = field(default_factory=list)
    Vector: List[float] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "Title": self.Title,
            "Genres": self.Genres,
            "Tags": self.Tags,
            "Description": self.Description,
            "Vector": self.Vector
        }