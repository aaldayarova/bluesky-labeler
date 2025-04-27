import json, requests, os, sys, csv
from atproto import Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pylabel.label import post_from_url, did_from_handle

# Environmental variables
SE_USER = os.getenv("SE_USER")
SE_SECRET = os.getenv("SE_SECRET")
SE_URL    = "https://api.sightengine.com/1.0/check.json"
SE_MODELS = "genai"
VERSION = "1.2.2"
U_API_KEY = os.getenv("U_API_KEY")
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

# Helper function to extract post image from Bluesky URL and classify using Sightengine ("AI-generated")
def extract_bluesky_image (url):
    try:
        parts = url.strip('/').split('/')
        handle = parts[-3]
        rkey = parts[-1]
        did = did_from_handle(handle)

        record = client.com.atproto.repo.get_record({
            'repo': did,
            'collection': 'app.bsky.feed.post',
            'rkey': rkey
        })
        embed = record['value'].embed
        if embed and hasattr(embed, "images"):
            cid = embed.images[0].image.ref.link
            img_url = f"https://bsky.social/xrpc/com.atproto.sync.getBlob?did={did}&cid={cid}"
            
            # Follow the redirect to get the final URL
            response = requests.get(img_url, allow_redirects=False)
            if 300 <= response.status_code < 400:
                final_url = response.headers['Location']
                return final_url
            return img_url
            
    except Exception as e:
        print(f"Error fetching image from Bluesky URL {url}: {e}")
        return None

if __name__ == "__main__":
    # Open CSV test file
    path = "./test-posts.csv"
    path_results = "./test-posts-results.csv"
    updated_rows = []

    try:
        with open(path, newline="", encoding="utf-8") as file:
            file = csv.reader(file)
            header = next(file) # Ignore the header row
            updated_rows.append(header)

            for line in file:
                policy_label = None # Reset our label
                if line:
                    post_url = line[0].strip().lower() # URL to Bluesky post

                    # Image classification workflow
                    img_url = extract_bluesky_image(post_url)
                    params = {
                    'url': img_url,
                    'workflow': 'wfl_ilfj9O1Bt1d4JCu5hLKzi',
                    'api_user': SE_USER,
                    'api_secret': SE_SECRET
                    }
                    r = requests.get('https://api.sightengine.com/1.0/check-workflow.json', params=params)
                    image_output = json.loads(r.text)
                    ai_generated_probability = image_output['type']['ai_generated']
                    print("The probability that image is AI-generated: ", ai_generated_probability)

                    # Text classification workflow
                    classifier1 = "Topics"
                    classifier2 = "Society Topics"
                    text_output1 = classify_text(post_url, classifier1)[0]['classification']
                    text_output2 = classify_text(post_url, classifier2)[0]['classification']
                    society_probability = None
                    politics_probability = None
                    for category in text_output1:
                        if category['className'] == 'Society':
                            society_probability = category['p']
                            break
                    for category in text_output2:
                        if category['className'] == 'Politics':
                            politics_probability = category['p']
                            break
                    print("The probability that text is about society: ", society_probability)
                    print("The probability that text is specifically about politics: ", politics_probability)
                    print("--------------")

                    # Calculate label
                    if ai_generated_probability >= 0.75 and (society_probability >= 0.5 or politics_probability >= 0.5):
                        policy_label = 'Potentially AI-generated political information'
                    
                    # Update the line with the policy label
                    if policy_label:
                        # Check if "Labels" column already has entries
                        if line[1] == "[]":
                            line[1] = f"[\"{policy_label}\"]"
                        else:
                            # Remove the closing bracket, add the new label, and close the bracket again
                            labels = line[1][:-1]  # Remove closing bracket
                            line[1] = f"{labels}, \"{policy_label}\"]"
                
                updated_rows.append(line)
            
        # Write the updated content back to the CSV file
        with open(path_results, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
                    
    except Exception as e:
        print(f"Error reading file {path}: {e}")