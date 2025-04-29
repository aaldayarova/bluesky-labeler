# Bluesky labeler for detecting AI-generated political posts
This is a labeler for the social media platform, Bluesky, that detects posts potentially containing AI-generated information about society and politics. This was built as a final project for Cornell Tech's class on Trust and Safety: Platforms, Policies, Products.

## Tools used
- AT Protocol SDK, which is documented [here](https://atproto.blue/en/latest/)
- uClassify to classify the content of text in posts, documented [here](https://www.uclassify.com/)
- SightEngine to detect AI-generated images in posts, documented [here](https://sightengine.com/image-moderation)

## Automated labeler
The file titled `policy_proposal_labeler.py` contains the labeler implementation.
To run the labeler, your working directory must be inside the `policy-labeler` folder.
Simply run `python3 policy_proposal_labeler.py` to see the labeler running on the test set `test-posts.csv`,
the output of which will be saved in `test-posts-results.csv`. The `__init__` would need to be changed
to see the labeler in action for a specific Bluesky URL.

## Testing
We provide a testing set in `test-posts.csv`. We also provide manually labeled
`test-posts-labeled.csv` containing our team's (subjective) determinant of which posts
would need to be labeled and which would not. After running the labeler as mentioned above,
`test-posts-results.csv` will populate with our labeler's results.
