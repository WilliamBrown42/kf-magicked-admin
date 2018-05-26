import configparser
import os
import signal
import sys
import logging

# Look through these closer.
from server.server import Server
from server.managers.motd_updater import MotdUpdater
from chatbot.chatbot import Chatbot
from utils.text import str_to_bool
from utils.validation import validate_config
from utils.logger import logger
from colorama import init
init()

if not os.path.exists("./magicked_admin.conf"):
    logger.error("Configuration file not found")
    input("Press enter to exit...")
    sys.exit()

config = configparser.ConfigParser()
config.read("./magicked_admin.conf")

#if not validate_config(config):
#    sys.exit()

class MagickedAdministrator:
    def __init__(self):
        self.servers = []
        self.chatbots = []
        self.motd_updaters = []

        signal.signal(signal.SIGINT, self.terminate)

    def run(self):
        for server_name in config.sections():
<<<<<<< HEAD
            # Looks like this tosses the full config section to server
            config[server_name]["name"] = server_name
            server = Server(config[server_name])

            #self.servers.append(server)
            #server.start()

=======
            """
                    threading.Thread.__init__(self)

                    self.config = config

                    multiadmin_enabled = str_to_bool(
                        config["multiadmin_enabled"]
                    )
                    motd_scoreboard = str_to_bool(
                        config["motd_scoreboard"]
                    )
                    self.operators = \
                        config["operators"].strip().split("\n")
                    self.operator_commands = \
                        config["operator_commands"].strip().split("\n")
                    self.help_text = \
                        config["help_text"]

                    # Change the shit to deal with web int here
                    web_interface = WebInterface(
                        config["address"],
                        config["username"],
                        config["password"],
                        multiadmin_enabled
                    )
                    self.web_admin = WebAdmin(web_interface, config["game_password"])

                    self.chat = Chat(
                        web_interface,
                        operators=self.operators,
                        server_name=config["name"]
                    )
                    chatbot = Chatbot(self.chat, config["address"] + "@" + config["name"])
                    self.chat.add_listener(chatbot)

                    self.database_controller = DatabaseController(config["name"])
                    self.database_queries = DatabaseQueries(self.database_controller.cur)

                    self.data_logger = DataLogger(web_interface, self.database_controller)
                    self.data_logger.add_listener(chatbot)

                    # Could be detached from server by passing in op list
                    commands = build_command_map(
                        self,
                        chatbot,
                        self.operator_commands
                    )
                    chatbot.set_commands(commands)

                    print("INFO: Initialising server " + config["name"] + " succeeded")
                    self.exit_flag = threading.Event()
            """
            # Changing the log level to the level specified in the config file
            logger.setLevel(logging.getLevelName(config[server_name]["log_level"]))
            address = config[server_name]["address"]
            user = config[server_name]["username"]
            password = config[server_name]["password"]
            game_password = config[server_name]["game_password"]
            motd_scoreboard = str_to_bool(
                config[server_name]["motd_scoreboard"]
            )
            scoreboard_type = config[server_name]["scoreboard_type"]
            level_threshhold = config[server_name]["level_threshold"]
            enable_greeter = str_to_bool(
                config[server_name]["enable_greeter"]
            )

            max_players = config[server_name]["max_players"]

            # Double check this one
            server = Server(server_name, address, user, password,
                            game_password, level_threshhold, max_players)

            self.servers.append(server)

            if motd_scoreboard:
                motd_updater = MotdUpdater(server, scoreboard_type)
                motd_updater.start()
                self.motd_updaters.append(motd_updater)

            cb = Chatbot(server, greeter_enabled=enable_greeter)
            server.chat.add_listener(cb)
            self.chatbots.append(cb)

        print("Initialisation complete")

>>>>>>> master
    def terminate(self, signal, frame):
        print("Terminating, saving data...")
        for server in self.servers:
            server.write_all_players(final=True)
            server.write_game_map()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    application = MagickedAdministrator()
    application.run()

    sys.exit(0)
