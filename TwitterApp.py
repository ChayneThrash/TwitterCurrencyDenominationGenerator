__author__ = 'Chayne'
import requests, json, sys
from requests_oauthlib import OAuth1
from GetChangeAmounts import generateChangeString
import Settings
from time import sleep
from ssl import SSLError
import socket


class ChangeGeneratorTwitterApp:
    def __init__(self):
        self.oauth = OAuth1(Settings.CONSUMER_KEY, client_secret=Settings.CONSUMER_SECRET,
                            resource_owner_key=Settings.TOKEN_KEY,
                            resource_owner_secret=Settings.TOKEN_SECRET, signature_type='auth_header')
        self.last_error = None
        self.network_error_delay = 0
        self.general_http_error_delay = 5
        self.http_420_error_delay = 60
        self.num_server_overload_errors = 0
        self.num_420_errors = 0

    def runApp(self):
        while True:
            self.__sleepBasedOnLastError()

            try:
                stream = self.__connectToStream()
                for line in stream.iter_lines():
                    if line:  # filter out keep-alive new lines
                        stream.raise_for_status()  # if an http error occurs during streaming, raise an exception
                        print line
                        self.__processResponse(json.loads(line))

            except (requests.ConnectionError, SSLError, socket.error):
                print 'TCP/IP error has occurred. Attempting to reconnect.'
                self.last_error = 'TCP/IP'
                continue
            except requests.HTTPError:
                if stream.status_code == 420:
                    self.last_error = '420'
                elif stream.status_code == 503:
                    print '503 error has occurred. Attempting to reconnect.'
                    self.last_error = 'Server Overload'
                else: # Twitter doesn't like something we are sending. Must be fixed.
                    print 'The following HTTP error code was received: ', stream.status_code
                    print 'This error must be fixed. Application cannot connect.'
                    sys.exit(1)
                continue
            except Exception as ex:
                print 'The following unexpected error occurred:'
                print ex
                sys.exit(1)

    def __sleepBasedOnLastError(self):
        if self.last_error is None:
            return
        elif self.last_error == 'TCP/IP':
            sleep(self.network_error_delay)
            self.network_error_delay += 0.25 if (self.network_error_delay != 16) else 0
            self.general_http_error_delay = 0
            self.http_420_error_delay = 60
        elif self.last_error == '420':
            sleep(self.http_420_error_delay)
            self.http_420_error_delay *= 2
            self.network_error_delay = 0
            self.general_http_error_delay = 0
        else:
            sleep(self.general_http_error_delay)
            self.general_http_error_delay *= 2 if (self.general_http_error_delay != 320) else 1
            self.network_error_delay = 0
            self.http_420_error_delay = 0

    def __connectToStream(self):
        stream_url = 'https://userstream.twitter.com/1.1/user.json'
        return requests.get(stream_url, auth=self.oauth, stream=True, timeout=90)

    def __processResponse(self, response):
        if ('direct_message' in response) and (self.__messageIsFromOtherUser(response)):
            received_message = response['direct_message']
            self.__respond(received_message)

    def __messageIsFromOtherUser(self, direct_message):
        return direct_message['direct_message']['sender']['screen_name'] != Settings.TWITTER_USER_NAME

    def __respond(self, received_message):
        direct_message_url = 'https://api.twitter.com/1.1/direct_messages/new.json'
        direct_message_params = dict(text=generateChangeString(received_message['text']),
                                     user_id=received_message['sender']['id'])
        requests.post(direct_message_url, params=direct_message_params, auth=self.oauth)


if __name__ == '__main__':
    ChangeGeneratorTwitterApp().runApp()
