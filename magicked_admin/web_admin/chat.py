import logging
from lxml import html
from colorama import init
from termcolor import colored

init()

# Add logger import
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)


class Listener(object):
    """
        Abstract for making classes that can receive messages from Chat.
        Supply:
            receive_message(self, username, message, admin):
    """

    def receive_message(self, username, message, admin):
        raise NotImplementedError("Listener.receive_message() not implemented")


class Chat:
    def __init__(self, web_interface, operators=None,
                 server_name="unnamed"):

        self.__web_interface = web_interface
        self.__listeners = []

        self.__print_messages = True
        self.silent = False
        self.server_name = server_name
        self.operators = operators if operators else []

    def poll(self):
        username_pattern = "//span[starts-with(@class,\'username\')]/text()"
        user_type_pattern = "//span[starts-with(@class,\'username\')]/@class"
        message_pattern = "//span[@class=\'message\']/text()"

        response = self.__web_interface.get_new_messages()

        if response.text:
            # trailing new line ends up in list without the strip
            messages_html = response.text.strip().split("\r\n\r\n")

            for message_html in messages_html:
                message_tree = html.fromstring(message_html)

                username = message_tree.xpath(username_pattern)[0]
                user_type = message_tree.xpath(user_type_pattern)[0]
                message = message_tree.xpath(message_pattern)[0]

                admin = True if \
                    "admin" in user_type or username in self.operators \
                    else False

                self.handle_message(username, message, admin)

    """
    def handle_message(self, username, message, admin):

        if self.print_messages and username != "server":
            print_line = username + "@" + self.server.name +  ": " + message

            if command:
                print_line = colored(print_line, 'green')
            elif username == self.server.username:
                print_line = colored(print_line, 'white')
            else:
                print_line = colored(print_line, 'yellow')
            print(print_line)
    """

    def handle_message(self, username, message, admin, internal=False):
        command = True if message[0] == '!' else False

        # What was internal? Just needs that and to add the colors
        if self.__print_messages and not internal:
            print_line = username + "@" + self.server_name + ": " + message
            if command:
                print_line = colored(print_line, 'green')
            else:
                print_line = colored(print_line, 'yellow')
            print(print_line)

        if internal:
            logger.debug("Internal message received: {}".format(message))

        for listener in self.__listeners:
            listener.receive_message(username, message, admin)

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def submit_message(self, message):
        if self.silent:
            return

        message_payload = {
            'ajax': '1',
            'message': message,
            'teamsay': '-1'
        }

        return self.__web_interface.post_message(message_payload)