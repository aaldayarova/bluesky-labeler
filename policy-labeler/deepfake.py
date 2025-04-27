import json, requests, os, sys
from atproto import Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pylabel.label import post_from_url

# Environmental variables
SE_USER = "731374990"
SE_SECRET = "co72s3ujppojYoEAgQMCe4sQk6uPbGvA"
SE_URL    = "https://api.sightengine.com/1.0/check.json"
SE_MODELS = "genai"
VERSION = "1.2.2"
U_API_KEY = "xo1p9bRwz3e9"
U_URL = "https://api.uclassify.com/v1"

client = Client()

# -*- coding: utf-8 -*-
"""
Copyright (c) 2017 Sightengine
http://sightengine.com/
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'SE-SDK-Python ' + VERSION,
    }
)

# Helper function to extract post text from Bluesky URL and classify using uClassify classifier ("Topics" or "Society Topics")
def classify_text(post_url, classifier, username="uclassify"):
    """
    Classify text using a specific uClassify classifier
    
    Args:
        post_url (str): The url to Bluesky post to classify
        classifier (str): The classifier to use
        username (str): The username of the classifier owner (default is "uclassify" for public classifiers)
    
    Returns:
        dict: Classification results
    """
    # Construct the endpoint URL
    url = f"{U_URL}/{username}/{classifier}/classify"

    # Retrieve the post text from URL
    post = post_from_url(client, post_url)
    post_text = post.value.text
    
    # Prepare the request headers
    headers = {
        "Authorization": f"Token {U_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the request payload
    payload = {
        "texts": [post_text]
    }
    
    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    params = {
    'url': 'https://img.freepik.com/premium-photo/scary-conceptual-image-bloody-knife-hand_894218-5746.jpg',
    'workflow': 'wfl_ilfj9O1Bt1d4JCu5hLKzi',
    'api_user': SE_USER,
    'api_secret': SE_SECRET
    }
    r = requests.get('https://api.sightengine.com/1.0/check-workflow.json', params=params)
    image_output = json.loads(r.text)
    print(image_output)

    print("------------")

    post_url = 'https://bsky.app/profile/newrepublic.com/post/3lnqevchm3r2b'
    classifier = "Society Topics"
    text_output = classify_text(post_url, classifier)
    print(f"Post classification probabilities: {text_output}")