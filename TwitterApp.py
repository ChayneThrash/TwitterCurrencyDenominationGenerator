__author__ = 'Chayne'
import requests, json, sys, thread, Queue, traceback, socket
from requests_oauthlib import OAuth1
from time import sleep
from ssl import SSLError
import Settings
from GetChangeAmounts import generateChangeString
import AppMessageHandler


def messageIsFromOtherUser(direct_message):
    return direct_message['direct_message']['sender']['screen_name'] != Settings.TWITTER_USER_NAME


# This class is responsible for running the twitter application. It functions by connecting to
# a user stream and responding whenever a direct message is received.
class ChangeGeneratorTwitterApp:

    NETWORK_ERROR_INIT_DELAY = 0
    SERVER_OVERLOAD_INIT_DELAY = 5
    HTTP_420_INIT_DELAY = 60

    def __init__(self):
        self.oauth = OAuth1(Settings.CONSUMER_KEY, client_secret=Settings.CONSUMER_SECRET,
                            resource_owner_key=Settings.TOKEN_KEY,
                            resource_owner_secret=Settings.TOKEN_SECRET, signature_type='auth_header')
        self.last_error = None
        self.network_error_delay = ChangeGeneratorTwitterApp.NETWORK_ERROR_INIT_DELAY
        self.server_overload_error_delay = ChangeGeneratorTwitterApp.SERVER_OVERLOAD_INIT_DELAY
        self.http_420_error_delay = ChangeGeneratorTwitterApp.HTTP_420_INIT_DELAY
        self.message_queue = Queue.Queue()
        self.message_handler = AppMessageHandler.AppMessageHandler(oauth=self.oauth, queue=self.message_queue)

    def runApp(self):
        while True:
            self.__sleepBasedOnLastError()
            thread.start_new_thread(self.message_handler.handleMessages, ())

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
                else:  # Twitter doesn't like something we are sending. Must be fixed.
                    print 'The following HTTP error code was received: ', stream.status_code
                    print 'This error must be fixed. Application cannot connect.'
                    sys.exit(1)
                continue
            except Exception as ex:
                print 'The following unexpected error occurred:', ex
                print traceback.format_exc()  # This prints the stack trace.
                sys.exit(1)

    def __sleepBasedOnLastError(self):
        if self.last_error is None:
            return
        elif self.last_error == 'TCP/IP':
            sleep(self.network_error_delay)
            self.network_error_delay += 0.25 if (self.network_error_delay != 16) else 0
            self.server_overload_error_delay = ChangeGeneratorTwitterApp.SERVER_OVERLOAD_INIT_DELAY
            self.http_420_error_delay = ChangeGeneratorTwitterApp.HTTP_420_INIT_DELAY
        elif self.last_error == '420':
            sleep(self.http_420_error_delay)
            self.http_420_error_delay *= 2
            self.network_error_delay = ChangeGeneratorTwitterApp.NETWORK_ERROR_INIT_DELAY
            self.server_overload_error_delay = ChangeGeneratorTwitterApp.SERVER_OVERLOAD_INIT_DELAY
        else:
            sleep(self.server_overload_error_delay)
            self.server_overload_error_delay *= 2 if (self.server_overload_error_delay != 320) else 1
            self.network_error_delay = ChangeGeneratorTwitterApp.NETWORK_ERROR_INIT_DELAY
            self.http_420_error_delay = ChangeGeneratorTwitterApp.HTTP_420_INIT_DELAY

    def __connectToStream(self):
        stream_url = 'https://userstream.twitter.com/1.1/user.json'
        return requests.get(stream_url, auth=self.oauth, stream=True, timeout=90)

    def __processResponse(self, response):
        if ('direct_message' in response) and (messageIsFromOtherUser(response)):
            received_message = response['direct_message']
            self.__respond(received_message)

    def __respond(self, received_message):
        direct_message_params = dict(text=generateChangeString(received_message['text']),
                                     user_id=received_message['sender']['id'])
        self.message_queue.put(direct_message_params)


if __name__ == '__main__':
    ChangeGeneratorTwitterApp().runApp()
