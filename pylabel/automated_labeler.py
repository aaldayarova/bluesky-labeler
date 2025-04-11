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

        # Milestone 3
        self.news = self.get_news_labels(os.path.join(input_dir, "news-domains.csv"))
     
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

        # Milestone 2
        # TODO: Check if the post contains any of the words in the list
        try:
            post = post_from_url(self.client, url)
            text = post.value.text
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