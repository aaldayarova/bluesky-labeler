"""Implementation of automated moderator"""

from typing import List
from atproto import Client
import csv
import os
from .label import post_from_url
from perception.hashers.image import PHash

T_AND_S_LABEL = "t-and-s"
DOG_LABEL = "dog"
THRESH = 0.3

T_AND_S_WORD_FILE = "t-and-s-words.csv"
T_AND_S_DOMAIN_FILE = "t-and-s-domains.csv"
NEW_LABEL_FILE = "news-domains.csv"
DOG_DIR = "dog-list-images"

class AutomatedLabeler:
    """Automated labeler implementation"""

    def __init__(self, client: Client, input_dir):
        self.client = client
        self.input_dir = input_dir

        # Milestone 2
        self.words = self.get_csv(os.path.join(input_dir, T_AND_S_WORD_FILE))
        self.domains = self.get_csv(os.path.join(input_dir, T_AND_S_DOMAIN_FILE))

        # Milestone 3
        self.news = self.get_news_labels(os.path.join(input_dir, NEW_LABEL_FILE))

        # Milestone 4
        self.pHash = PHash()
        self.dog_image_hashes = []
        for file in os.listdir(os.path.join(input_dir, DOG_DIR)):
            if not file.endswith(".jpg") and not file.endswith(".png") and not file.endswith(".jpeg"):
                continue
            
            # Hash Dog Image
            dogImage = os.path.join(input_dir, DOG_DIR, file)
            dogHash = self.pHash.compute(dogImage)
            self.dog_image_hashes.append(dogHash)
     
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
    
    # Milestone 3
    # Get News Labels
    def get_news_labels(self, path: str) -> List[str]:
        """
        Load a CSV file and return the list of labels
        """
        news_labels = {}
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                for row in reader:
                    if row and len(row) >= 2:
                        domain = row[0].strip().lower()
                        label = row[1].strip().lower()
                        news_labels[domain] = label
        except Exception as e:
            print(f"Error reading file {path}: {e}")
        return news_labels
    
    def moderate_post(self, url: str) -> List[str]:
        """
        Apply moderation to the post specified by the given url
        """

        try:
            post = post_from_url(self.client, url)
            text = post.value.text
            embedded = post.value.embed
            print(embedded)
        except Exception as e:
            print(f"Error fetching post {url}: {e}")
            return []

        
        lower_text = text.lower()
        labels = set()

        # Milestone 2
        # Check if the post contains any of the words in the list
        for word in self.words:
            if word in lower_text:
                labels.add(T_AND_S_LABEL)
        
        for domain in self.domains:
            if domain in lower_text:
                labels.add(T_AND_S_LABEL)

        # Milestone 3
        # Check if post has any News Domains / Sources
        for domain, source in self.news.items():
            if domain in lower_text:
                labels.add(source)

        return list(labels)