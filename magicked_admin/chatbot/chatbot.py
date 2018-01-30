from web_admin.data_logger import Listener

from os import path

from utils.text import trim_string, millify


class Chatbot(Listener):
    
    def __init__(self, chat, command_map, name):
        #self.server = server
        self.name = name
        self.chat = chat
        self.command_map = command_map
        # The in-game chat can fit 21 Ws horizontally
        self.word_wrap = 21
        self.max_lines = 7

        self.silent = False
        
        if path.exists(self.name + ".init"):
            self.execute_script(self.name + ".init")

        print("INFO: Bot on server " + self.name + " initialised")

    def receive_message(self, username, message, admin=False):
        if message[0] == '!':
            # Drop the '!' because its no longer relevant
            args = message[1:].split(' ')
            self.command_handler(username, args, admin)

    def command_handler(self, username, args, admin=False):
        if args == None or len(args) == 0:
            return
        if args[0] in self.commands.command_map:
            command = self.commands.command_map[args[0]]
            response = command.execute(username, args, admin)
            if not self.silent:
                self.chat.submit_message(response)
        elif username != "server" and not self.silent:
            self.chat.submit_message("Sorry, I didn't understand that request.")

    def execute_script(self, file_name):
        print("INFO: Executing script: " + file_name)
        with open(file_name) as script:
            for line in script:
                print("\t\t" + line.strip())
                args = line.split()
                self.command_handler("server", args, admin=True)
