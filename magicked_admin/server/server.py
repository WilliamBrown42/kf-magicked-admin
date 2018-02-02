import threading

from chatbot.chatbot import Chatbot
from chatbot.commands.command_map import build_command_map

from web_admin.web_admin import WebAdmin
from web_admin.web_interface import WebInterface
from web_admin.chat import Chat
from web_admin.data_logger import DataLogger

from database.controller import DatabaseController
from database.queries import DatabaseQueries

from utils.text import str_to_bool


class Server(threading.Thread):

    def __init__(self, config):
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

    def run(self):
        while not self.exit_flag.wait(3):
            self.chat.poll()
            self.data_logger.poll()

    def terminate(self):
        self.exit_flag.set()
        print("INFO: Terminating thread [server: " + self.config["name"] + "]")
