"""Implementation of automated moderator"""

from typing import List
from atproto import Client
import csv
import os
from .label import post_from_url

T_AND_S_LABEL = "t-and-s"
DOG_LABEL = "dog"
THRESH = 0.3

class AutomatedLabeler:
    """Automated labeler implementation"""

    def __init__(self, client: Client, input_dir):
        self.client = client
        self.input_dir = input_dir

        # Milestone 2
        self.words = self.get_csv(os.path.join(input_dir, "t-and-s-words.csv"))
        self.domains = self.get_csv(os.path.join(input_dir, "t-and-s-domains.csv"))
     
    # Milestone 2
    def get_csv(self, path: str) -> List[str]:
        """
        Load a CSV file and return the list of labels
        """
        items = []
        try:
            with open(path, newline='', encoding='utf-8') as file:
                file = csv.reader(file)
                for line in file:
                    if line:
                        value = line[0].strip().lower()
                        items.append(value)
        except Exception as e:
            print(f"Error reading file {path}: {e}")
        return items
   
    def moderate_post(self, url: str) -> List[str]:
        """
        Apply moderation to the post specified by the given url
        """

        # Milestone 2
        # TODO: Check if the post contains any of the words in the list
        try:
            post = post_from_url(self.client, url)
            text = post.value.text
        except Exception as e:
            print(f"Error fetching post {url}: {e}")
            return []

        lower_text = text.lower()
        # print(lower_text)
        # labels = []

        # applyLabel = False

        # for word in self.words:
        #     if word in lower_text:
        #         applyLabel = True
            
        # for domain in self.domains:
        #     if domain in lower_text:
        #         applyLabel = True

        # if applyLabel:
        #     labels.append(T_AND_S_LABEL)
        
        for word in self.words:
            # print(f"The word is {word}")
            if word in lower_text:
                return [T_AND_S_LABEL]
        
        for domain in self.domains:
            # print(f"The domain is {domain}")
            if domain in lower_text:
                return [T_AND_S_LABEL]

        return []