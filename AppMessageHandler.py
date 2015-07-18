__author__ = 'Chayne'
import requests, traceback, json
from TwitterApp import messageIsFromOtherUser


# This class is responsible for sending message as the app receives them.
# The class contains a queue shared by the app so that when the app
# prepares information to send, it can simply queue it up and let this class
# handle the rest.
class AppMessageHandler:
    def __init__(self, oauth, queue):
        self.oauth = oauth
        self.message_queue = queue

    def __directMesssageSentSuccessfully(self, response_content):
        try:
            message_json = json.loads(response_content)
            return True if ('direct_message' in message_json) and (not messageIsFromOtherUser(message_json)) else False
        except Exception as ex:
            print 'The following error occurred when sending: ', ex
            print traceback.format_exc()  # This prints the stack trace.
            return False

    def handleMessages(self):
        direct_message_url = 'https://api.twitter.com/1.1/direct_messages/new.json'
        while True:
            last_message_sent = True
            while not self.message_queue.empty():
                if last_message_sent:
                    message = self.message_queue.get()
                response = requests.post(url=direct_message_url, params=message, auth=self.oauth)
                print response.content
                last_message_sent = self.__directMesssageSentSuccessfully(response.content)