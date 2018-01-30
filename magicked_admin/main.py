import configparser
import os
import signal
import sys

from chatbot.chatbot import Chatbot
from server.motd_updater import MotdUpdater
from utils.text import str_to_bool
from web_admin.web_admin import WebAdmin
from web_admin.web_interface import WebInterface

from server.server import Server

DEBUG = True

if not os.path.exists("./magicked_admin.conf"):
    sys.exit("Configuration file not found.")
config = configparser.ConfigParser()
config.read("./magicked_admin.conf")


class MagickedAdministrator():
    
    def __init__(self):
        self.data_loggers = []
        self.chatbots = []
        self.motd_updaters = []
        
        signal.signal(signal.SIGINT, self.terminate)

    def run(self):

        for server_name in config.sections():
            config[server_name]["name"] = server_name
            server = Server(config[server_name])
            print(server.name)
            '''address = config[server_name]["address"] 
            user = config[server_name]["username"]
            password = config[server_name]["password"]
            game_password = config[server_name]["game_password"]
            motd_scoreboard = str_to_bool(config[server_name]["motd_scoreboard"])
            scoreboard_type = config[server_name]["scoreboard_type"]

            multiadmin_enabled = str_to_bool(config[server_name]["multiadmin_enabled"])

            operators = config[server_name]["operators"]
            operator_commands = config[server_name]["operator_commands"]
            print(operators)
            print(operator_commands)

            web_interface = WebInterface(address, user, password,
                                         str_to_bool(multiadmin_enabled))
            web_admin = WebAdmin(web_interface, game_password)
            server = Server(server_name, address, user, password,
                            game_password, hashed=multiadmin_enabled)
            self.servers.append(server)
                
            if motd_scoreboard:
                motd_updater = MotdUpdater(server, scoreboard_type)
                motd_updater.start()
                self.motd_updaters.append(motd_updater)

            cb = Chatbot(server)
            server.chat.add_listener(cb)
            self.chatbots.append(cb)'''

        print("INFO: Initialisation complete\n")
            
    def terminate(self, signal, frame):
        print("\nINFO: Terminating...")
        for server in self.servers:
            server.terminate()
        #for cb in self.chatbots:
        #    cb.terminate()
        for motd_updater in self.motd_updaters:
            motd_updater.terminate()


if __name__ == "__main__":
    application = MagickedAdministrator()
    application.run()

    sys.exit(0)

