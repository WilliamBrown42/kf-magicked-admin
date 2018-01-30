from chatbot.chatbot import Chatbot

from web_admin.web_admin import WebAdmin
from web_admin.web_interface import WebInterface
from web_admin.chat import Chat
from web_admin.data_logger import DataLogger

from database.controller import DatabaseController

from utils.text import str_to_bool


class Server:

    def __init__(self, config):
        self.name = config["name"]
        self.address = config["address"]
        self.username = config["username"]
        self.password = config["password"]
        self.game_password = config["game_password"]
        self.motd_scoreboard = str_to_bool(
            config["motd_scoreboard"]
        )
        self.multiadmin_enabled = str_to_bool(
            config["multiadmin_enabled"]
        )
        self.chat_refresh_rate = config["chat_refresh_rate"]
        self.info_refresh_rate = config["info_refresh_rate"]
        self.logger_refresh = config["logger_refresh"]

        self.operators = config["operators"].strip().split("\n")
        self.operator_commands = config["operator_commands"].strip().split("\n")
        print(self.operators)
        print(self.operator_commands)

        web_interface = WebInterface(
            self.address,
            self.username,
            self.password,
            self.multiadmin_enabled
        )

        self.web_admin = WebAdmin(
            web_interface,
            self.game_password
        )

        chat = Chat(
            web_interface,
            operators=self.operators,
            server_name=self.name,
            time_interval=self.chat_refresh_rate
        )

        self.chatbot = Chatbot(chat, self)

        self.database_controller = DatabaseController(self.name)
        self.data_logger = DataLogger(web_interface, DatabaseController,
                                      self.logger_refresh)
