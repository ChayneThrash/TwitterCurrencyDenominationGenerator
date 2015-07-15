__author__ = 'Chayne'
import requests
import json
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
from CurrencyDenominationGenerator import *
import Settings


class CurrencyDenominationTwitterApp:
    def __init__(self):
        self.oauth = OAuth1(Settings.CONSUMER_KEY, client_secret=Settings.CONSUMER_SECRET, resource_owner_key=Settings.TOKEN_KEY,
                            resource_owner_secret=Settings.TOKEN_SECRET, signature_type='auth_header')

    def runApp(self):
        stream = self.__connectToStream()
        for line in stream.iter_lines():
            if line:  # filter out keep-alive new lines
                print line
                self.__processResponse(json.loads(line))

    def __connectToStream(self):
        stream_url = 'https://userstream.twitter.com/1.1/user.json'
        return requests.post(stream_url, auth=self.oauth, stream=True)

    def __processResponse(self, response):
        if ('direct_message' in response) and (self.__senderIsNotApp(response)):
            received_message = response['direct_message']
            self.__respond(received_message)

    def __senderIsNotApp(self, direct_message):
        return direct_message['direct_message']['sender']['screen_name'] != Settings.TWITTER_USER_NAME

    def __respond(self, received_message):
        direct_message_url = 'https://api.twitter.com/1.1/direct_messages/new.json'
        direct_message_params = dict(text = generateCurrencyDenominationsString(received_message['text']),
                                     user_id = received_message['sender']['id'])
        requests.post(direct_message_url, params=direct_message_params, auth=self.oauth)



if __name__ == '__main__':
    CurrencyDenominationTwitterApp().runApp()