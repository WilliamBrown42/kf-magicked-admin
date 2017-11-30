from os import path
import threading

import requests, sys
from hashlib import sha1
from lxml import html
from time import sleep

from server.managers.server_mapper import ServerMapper

from database.controller import DatabaseController
from web_admin.web_admin import WebAdmin
from web_admin.chat import Chat


class Server(threading.Thread):
   
    def __init__(self, name, web_interface):
        self.name = name
        self.web_admin = WebAdmin(web_interface)
        self.chat = Chat(web_interface, name, time_interval=3)
        self.database = DatabaseController(name)

        self.player_records = []

        self.chat.start()

    def end_wave(self):
        self.chat.handle_message("server",
                                 "!end_wave " + str(self.game['wave']),
                                 admin=True, internal=True)
        for player in self.player_records:
            player.wave_kills = 0
            player.wave_dosh = 0

    def trader_open(self):
        self.chat.handle_message("server", "!t_open",
                                 admin=True, internal=True)

    def new_game(self):
        self.chat.handle_message("server", "!new_game",
                                 admin=True, internal=True)

    def get_player(self, username):
        for player in self.players:
            if player.username == username:
                return player
        return None

    def player_join(self, player):
        self.database.load_player(player)
        player.total_logins += 1
        self.players.append(player)
        self.chat.handle_message("server", "!p_join " + player.username, admin=True)
        print("INFO: Player " + player.username + " joined")        

    def player_quit(self, quit_player):
        for player in self.players:
            if player.username == quit_player.username:
                print("INFO: Player " + player.username + " quit")
                self.chat.handle_message("server", "!p_quit " + player.username, admin=True)
                self.database.save_player(player, final=True)
                self.players.remove(player)

    def write_all_players(self, final=False):
        print("INFO: Writing players")
        for player in self.players:
            self.database.save_player(player, final)

    def terminate(self):
        self.mapper.terminate()
        self.mapper.join()

        self.chat.terminate()
        self.chat.join()

        self.write_all_players(final=True)
