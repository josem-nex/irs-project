import json
import os


class Tag:
    """
    A class to extract tags from a JSON file and store them in a list.
    """
    def __init__(self):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.data_path = os.path.abspath(os.path.join(self.current_path, '..', '..', 'data'))
        self.scraper_path = os.path.abspath(os.path.join(self.data_path, 'scraper_result.json'))
        self.tags_output = os.path.abspath(os.path.join(self.data_path, 'tags.txt'))
        self.json_data = self.load_json()
        self.all_tags = self.extract_tags()

    def load_json(self):
        with open(self.scraper_path, "r") as f:
            return json.load(f)

    def extract_tags(self):
        """
        Extracts all tags from a JSON file and stores them in a list.   
        or loads the tags from the file if it exists. 
        Args:
          json_data: A list of dictionaries representing the JSON data. 
        Returns:
          A list of all tags.
        """
        if os.path.exists(self.tags_output):
            with open(self.tags_output, "r") as f:
                return [tag.strip().lower() for tag in f.readlines()]
            
        if not self.json_data:
            return Exception("No JSON data found.")
        
            
        all_tags = set()
        for item in self.json_data:
            tags = item.get("tags", [])
            all_tags.update(tags)
            
        self.save_tags(all_tags)
        
        return list(all_tags)

    def save_tags(self, all_tags):
        with open(self.tags_output, "w") as f:
            for tag in all_tags:
                f.write(tag.lower() + "\n")


