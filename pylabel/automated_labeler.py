# """Implementation of automated moderator"""

# from typing import List
# from atproto import Client
# import csv
# import os
# from .label import post_from_url
# from io import BytesIO
# from PIL import Image
# import requests
# import tempfile

# # Imports for Milestone 4
# from perception import hashers
# from .label import did_from_handle

# T_AND_S_LABEL = "t-and-s"
# DOG_LABEL = "dog"
# THRESH = 0.3

# T_AND_S_WORD_FILE = "t-and-s-words.csv"
# T_AND_S_DOMAIN_FILE = "t-and-s-domains.csv"
# NEW_LABEL_FILE = "news-domains.csv"
# DOG_DIR = "dog-list-images"


# class AutomatedLabeler:
#     """Automated labeler implementation"""

#     def __init__(self, client: Client, input_dir):
#         self.client = client
#         self.input_dir = input_dir

#         # Milestone 2
#         self.words = self.get_csv(os.path.join(input_dir, T_AND_S_WORD_FILE))
#         self.domains = self.get_csv(os.path.join(input_dir, T_AND_S_DOMAIN_FILE))

#         # Milestone 3
#         self.news = self.get_news_labels(os.path.join(input_dir, NEW_LABEL_FILE))

#         # Milestone 4
#         self.dogImageHashes = []
#         dog_images_dir = os.path.join(input_dir, DOG_DIR)
#         self.hasher = hashers.PHash()
    
#         for file in os.listdir(dog_images_dir):
#             if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
#                 continue
#             dogImage = os.path.join(dog_images_dir, file)
#             try:
#                 with Image.open(dogImage) as img:
#                     # Hashing images in csv
#                     img = img.convert("RGB")
#                     dogHash = self.hasher.compute(img) # Computes Hash from Image
#                     self.dogImageHashes.append(dogHash)

#                     # Hashing images in Bluesky
#                     # pulled_images = self.extract_bluesky_image()
#             except Exception as e:
#                 print(f"Error processing dog image {dogImage}: {e}")
    
#     # Helper function for Milestone 4 to extract image from Bluesky URL
#     def extract_bluesky_image (self, url: str):
#         try:
#             parts = url.strip('/').split('/')
#             handle = parts[-3]
#             rkey = parts[-1]
#             did = did_from_handle(handle)

#             record = self.client.com.atproto.repo.get_record({
#                 'repo': did,
#                 'collection': 'app.bsky.feed.post',
#                 'rkey': rkey
#             })
#             embed = record['value'].embed
#             if embed and hasattr(embed, "images"):
#                 cid = embed.images[0].image.ref.link
#                 img_url = f"https://bsky.social/xrpc/com.atproto.sync.getBlob?did={did}&cid={cid}"
#                 response = requests.get(img_url)
#                 response.raise_for_status()  # Raise an error for bad responses
#                 return Image.open(BytesIO(response.content))
#         except Exception as e:
#             print(f"Error fetching image from Bluesky URL {url}: {e}")
#             return None
    
#     # Milestone 2
#     def get_csv(self, path: str) -> List[str]:
#         """
#         Load a CSV file and return the list of labels
#         """
#         items = []
#         try:
#             with open(path, newline="", encoding="utf-8") as file:
#                 file = csv.reader(file)
#                 for line in file:
#                     if line:
#                         value = line[0].strip().lower()
#                         items.append(value)
#         except Exception as e:
#             print(f"Error reading file {path}: {e}")
#         return items

#     # Milestone 3
#     # Get News Labels
#     def get_news_labels(self, path: str) -> List[str]:
#         """
#         Load a CSV file and return the list of labels
#         """
#         news_labels = {}
#         try:
#             with open(path, newline="", encoding="utf-8") as f:
#                 reader = csv.reader(f)
#                 next(reader, None)  # Skip header
#                 for row in reader:
#                     if row and len(row) >= 2:
#                         domain = row[0].strip().lower()
#                         label = row[1].strip().lower()
#                         news_labels[domain] = label
#         except Exception as e:
#             print(f"Error reading file {path}: {e}")
#         return news_labels

#     def moderate_post(self, url: str) -> List[str]:
#         """
#         Apply moderation to the post specified by the given url
#         """

#         try:
#             post = post_from_url(self.client, url)
#             text = post.value.text
#             embedded = post.value.embed
#             print(embedded)
#         except Exception as e:
#             print(f"Error fetching post {url}: {e}")
#             return []

#         lower_text = text.lower()
#         labels = set()

#         # Milestone 2
#         # Check if the post contains any of the words in the list
#         for word in self.words:
#             if word in lower_text:
#                 labels.add(T_AND_S_LABEL)

#         for domain in self.domains:
#             if domain in lower_text:
#                 labels.add(T_AND_S_LABEL)

#         # Milestone 3
#         # Check if post has any News Domains / Sources
#         for domain, source in self.news.items():
#             if domain in lower_text:
#                 labels.add(source)


#         # Milestone 4
#         image = self.extract_bluesky_image(url)
#         if image:
#             try:
#                 with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
#                     image.save(temp_file, format="PNG")
#                     temp_file.flush()
#                     image_hash = self.hasher.compute(temp_file.name)
#                     for dog_hash in self.dogImageHashes:
#                         distance = self.hasher.compute_distance(image_hash, dog_hash)
#                         if distance <= THRESH:
#                             labels.add(DOG_LABEL)
#                             break
#             except Exception as e:
#                 print(f"Error processing image: {e}")
#         return list(labels)

# if __name__ == "__main__":
#     client = Client()
#     labeler_obj = AutomatedLabeler(client, "./labeler-inputs")
#     print(labeler_obj.extract_bluesky_image())
