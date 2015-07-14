__author__ = 'Chayne'
import requests
import json
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
from CurrencyDenominationGenerator import *

TWITTER_USER_NAME = 'smith2015_kevin'
CONSUMER_KEY = '2xbz3fkDvZl57K7jNv30jMgCT'
CONSUMER_SECRET = '3MmmeDnMuN9mUV6kCw3IAYfbxeWLl5J2fYDIiaJV40fPFvwTK8'
TOKEN_KEY = '3340282143-c3pn0lkxxOXll5ZReY6TyR5UWHv4ssbjy5H5ktF'
TOKEN_SECRET = 'UncL8lPDGdjCE1NaTlCAmQDAcXhCFuDlVhb60dKr8V31c'

oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=TOKEN_KEY, resource_owner_secret=TOKEN_SECRET, signature_type='auth_header')

stream_url = 'https://userstream.twitter.com/1.1/user.json'
direct_message_url = 'https://api.twitter.com/1.1/direct_messages/new.json'
direct_message_params = {'user_id' : 'temporary id', 'text' : 'temporary text'}

r = requests.post(stream_url, auth=oauth, stream=True)

for line in r.iter_lines():
    if line: # filter out keep-alive new lines
        stream_resp = json.loads(line)
        if ('direct_message' in stream_resp) and (stream_resp['direct_message']['sender']['screen_name'] != TWITTER_USER_NAME):
            message = stream_resp['direct_message']
            direct_message_params['text'] = generateCurrencyDenominationsString(message['text'])
            direct_message_params['user_id'] = stream_resp['direct_message']['sender']['id']
            requests.post(direct_message_url, params=direct_message_params, auth=oauth)
        print(line)