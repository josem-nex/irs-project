from dataclasses import dataclass, field
from typing import List

@dataclass
class GameOut:
    Title: str
    Description: str 
    Similarity: float
    Genres: List[str] = field(default_factory=list)
    Tags: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "Title": self.Title,
            "Genres": self.Genres,
            "Tags": self.Tags,
            "Description": self.Description,
            "Similarity": self.Similarity   
        }