import json, requests
from io import BytesIO

# Environmental variables
SE_USER = "731374990"
SE_SECRET = "co72s3ujppojYoEAgQMCe4sQk6uPbGvA"
SE_URL    = "https://api.sightengine.com/1.0/check.json"
SE_MODELS = "genai"
VERSION = "1.2.2"

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

class Check(object):
    def __init__(self, api_user, api_secret, *args):
        self.api_user = api_user
        self.api_secret = api_secret
        self.endpoint = 'https://api.sightengine.com/1.0/'
        self.modelsType = ''
        self.workflowId = "wfl_ilfj9O1Bt1d4JCu5hLKzi"

        if len(args) > 1:
            for arg in args:
                self.modelsType += arg + ','
            self.modelsType = self.modelsType[:-1]
        else:
            self.modelsType = args[0]

    def set_url(self, imageUrl):
        r = requests.get(self.endpoint + 'check.json', params={'models': self.modelsType, 'url': imageUrl, 'api_user': self.api_user, 'api_secret': self.api_secret, 'workflow_id': self.workflowId}, headers=headers)

        output = json.loads(r.text)
        return output

    def set_file(self, file):
        r = requests.post(self.endpoint + 'check.json', files={'media': open(file, 'rb')}, data={'models': self.modelsType, 'api_user': self.api_user,'api_secret': self.api_secret}, headers=headers)

        output = json.loads(r.text)
        return output

    def set_bytes(self, binaryImage):
        r = requests.post(self.endpoint + 'check.json', files={'media': BytesIO(binaryImage)}, data={'models': self.modelsType, 'api_user': self.api_user, 'api_secret': self.api_secret}, headers=headers)

        output = json.loads(r.text)
        return output

    def video(self, videoUrl, callbackUrl):
        r = requests.get(self.endpoint + 'video/check.json', params={'models': self.modelsType, 'callback_url': callbackUrl, 'stream_url': videoUrl, 'api_user': self.api_user, 'api_secret': self.api_secret}, headers=headers)

        output = json.loads(r.text)
        return output

    def video_sync(self, videoUrl):
        r = requests.get(self.endpoint + 'video/check-sync.json', params={'models': self.modelsType, 'stream_url': videoUrl, 'api_user': self.api_user, 'api_secret': self.api_secret}, headers=headers)

        output = json.loads(r.text)
        return output


class SightengineClient(object):
    modelVersions = {}

    def __init__(self, api_user, api_secret):
        self.api_user = api_user
        self.api_secret = api_secret
        self.endpoint = 'https://api.sightengine.com/'

    def feedback(self, model, modelClass, image):
        if not model:
            raise Exception('Please provide the version of the model ' + model)

        if image.lower().startswith(('http://', 'https://')):
            url = self.endpoint + '1.0/feedback.json'
            r = requests.get(url, params={'model': model, 'class': modelClass, 'url': image, 'api_user': self.api_user, 'api_secret': self.api_secret}, headers=headers)
        else:
            url =  self.endpoint + '1.0/feedback.json'
            r = requests.post(url, files={'media': open(image, 'rb')}, data={'model': model, 'class': modelClass, 'api_user': self.api_user, 'api_secret': self.api_secret}, headers=headers)

        output = json.loads(r.text)
        return output

    def check(self, *args):
        return Check(self.api_user,self.api_secret, *args)

if __name__ == "__main__":
    # client = SightengineClient(SE_USER, SE_SECRET)
    # output = client.check('genai').set_url('https://p.potaufeu.asahi.com/1831-p/picture/27695628/89644a996fdd0cfc9e06398c64320fbe.jpg')
    # print(output)
    params = {
    'url': 'https://img.freepik.com/premium-photo/scary-conceptual-image-bloody-knife-hand_894218-5746.jpg',
    'workflow': 'wfl_ilfj9O1Bt1d4JCu5hLKzi',
    'api_user': '731374990',
    'api_secret': 'co72s3ujppojYoEAgQMCe4sQk6uPbGvA'
    }
    r = requests.get('https://api.sightengine.com/1.0/check-workflow.json', params=params)

    output = json.loads(r.text)
    print(output)