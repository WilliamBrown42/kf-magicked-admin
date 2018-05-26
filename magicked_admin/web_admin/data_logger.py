import logging
from itertools import groupby
from collections import namedtuple
from utils.geolocation import get_country

from lxml import html

from web_admin.model.player import Player
from web_admin.model.game import Game

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ConstGame = namedtuple('Game', ['trader_open', 'zeds_total', 'zeds_dead',
                                'map_title', 'map_name', 'wave', 'length',
                                'difficulty', 'game_type'])

ConstPlayer = namedtuple('Player', ['username', 'perk', 'kills',
                                    'health', 'dosh', 'ping'])


class Listener(object):
    """
        Abstract for making classes that can receive messages from DataLogger.
        Supply:
            recieveMessage(self, username, message, admin):
    """

    def receive_message(self, username, message, admin):
        raise NotImplementedError("Listener.recieveMessage() not implemented")


class DataLogger:
    def __init__(self, web_interface, database_controller):
        self.__web_interface = web_interface
        self.__database = database_controller

        self.listeners = []

        self.players = []

        # map, difficulty, mode,
        self.game = Game(self.__database.open_game)

    def poll(self):
        response = self.__web_interface.get_server_info()
        info_tree = html.fromstring(response.content)

        players_now = self.__get_current_players(info_tree)
        game_now = self.__get_current_game(info_tree)

        self.__update_players(players_now)
        self.__update_game(game_now)

    def __update_game(self, game_now):
        if game_now.wave < self.game.wave:
            self.__event_new_game()
        elif game_now.wave > self.game.wave:
            self.__event_wave_start()
        if game_now.zeds_dead == game_now.zeds_total:
            # This will continue to spam "!wave end" when there are no players
            self.__event_wave_end()

        if game_now.trader_open and not self.game.trader_open:
            self.__event_trader_open()
        if not game_now.trader_open and self.game.trader_open:
            self.__event_trader_close()

        self.game.map.title = game_now.map_title
        self.game.map.name = game_now.map_name
        self.game.wave = game_now.wave
        self.game.length = game_now.length
        self.game.difficulty = game_now.difficulty
        self.game.zeds_dead = game_now.zeds_dead
        self.game.zeds_total = game_now.zeds_total
        self.game.game_type = game_now.game_type

    def __update_players(self, players_now):
        # Quitters
        for player in self.players:
            if player.username not in [p.username for p in players_now]:
                self.__event_player_quit(player)

        # Joiners
        for player in players_now:
            if player.username not in [p.username for p in self.players]:
                self.__event_player_join(player)

        for player in self.players:
            player_now = next(filter(
                lambda p: p.username == player.username, players_now
            ))
            player.kills = player_now.kills
            player.health = player_now.health
            player.ping = player_now.ping

            player.perk = player_now.perk
            player.total_kills += player_now.kills - player.kills

            player.wave_kills += player_now.kills - player.kills
            player.wave_dosh += player_now.dosh - player.dosh

            if player_now.dosh > player.dosh:
                player.game_dosh += player_now.dosh - player.dosh
                player.total_dosh += player_now.dosh - player.dosh

            else:
                player.total_dosh_spent += player.dosh - player_now.dosh
            player.dosh = player_now.dosh

    @staticmethod
    def __get_current_players(info_tree):
        players = []
        odds = info_tree.xpath('//tr[@class="odd"]//td/text()')
        evens = info_tree.xpath('//tr[@class="even"]//td/text()')
        player_rows = odds + evens

        player_rows = [list(group) for k, group in
                       groupby(player_rows, lambda x: x == "\xa0") if not k]

        for player_row in player_rows:
            if len(player_row) < 7:
                # Player is dead
                username, perk, dosh = player_row[:3]
                health = 0
                kills, ping = player_row[3:5]
            else:
                # Player is alive
                username, perk, dosh, health, kills, ping \
                    = player_row[:6]

            player = ConstPlayer(username, perk, int(kills),
                                 int(health), int(dosh), int(ping))
            players.append(player)
        return players

    @staticmethod
    def __get_current_game(info_tree):
        zed_status_pattern = "//dd[@class=\"gs_wave\"]/text()"
        zeds_dead, zeds_total = \
            info_tree.xpath(zed_status_pattern)[0].split("/")
        zeds_dead, zeds_total = int(zeds_dead), int(zeds_total)

        if zeds_dead == zeds_total and zeds_total > 1:
            trader_open = True
        else:
            trader_open = False

        zeds_total = int(zeds_total)
        zeds_dead = int(zeds_dead)

        dds = info_tree.xpath('//dd/text()')
        game_type = info_tree.xpath('//dl//dd/@title')[0]
        map_title = info_tree.xpath('//dl//dd/@title')[1]
        map_name = dds[0]
        wave, length = [int(val) for val in dds[7].split("/")]
        difficulty = dds[8]

        return ConstGame(trader_open, zeds_total, zeds_dead, map_title,
                         map_name, wave, length, difficulty, game_type)

    def get_player(self, username):
        for player in self.players:
            if player.username == username:
                return player

    def get_player_details(self, username):
        response = self.__web_interface.get_players()
        player_tree = html.fromstring(response.content)

        odds = player_tree.xpath('//tr[@class="odd"]//td/text()')
        evens = player_tree.xpath('//tr[@class="even"]//td/text()')

        player_rows = odds + evens

        player_rows = [list(group) for k, group in
                       groupby(player_rows, lambda x: x == "\xa0") if not k]

        print(str(player_rows))

        for player in player_rows:
            if player[0] == username:
                ip = player[2]
                steam_id = player[4]
                country, country_code = get_country(ip)
                return {
                    'steam_id': steam_id,
                    'ip': ip,
                    'country': country,
                    'country_code': country_code
                }

        logger.warning("Couldn't find player details for: {}".format(username))
        return {
                    'steam_id': "00000000000000000",
                    'ip': "0.0.0.0",
                    'country': "Unknown",
                    'country_code': "??"
                }

    def add_listener(self, listener):
        self.listeners.append(listener)

    def __send_message(self, message):
        print("DATA_LOGGER_MESG: " + message)
        for listener in self.listeners:
            listener.receive_message("%internal%", message, admin=True)

    def write_players(self):
        for player in self.players:
            self.__database.save_player(player)

    def __event_wave_end(self):
        self.__send_message("!wave_end")

    def __event_wave_start(self):
        self.__send_message("!wave_start")

    def __event_new_game(self):
        self.__database.close_game(self.game)
        self.game.game_id = self.__database.open_game(self.game)
        self.__send_message("!new_game")

    def __event_player_join(self, player):
        player_details = self.get_player_details(player.username)

        new_player = Player(
            player_details["steam_id"],
            player_details["country_code"],
            player_details["ip"],
            player.username)

        self.players.append(new_player)
        self.__database.open_session(new_player, self.game)

        self.__send_message("!player_join " + player.username)

    def __event_player_death(self, player):
        self.__send_message("!player_death " + player.username)

    def __event_player_quit(self, player):
        self.__send_message("!player_quit" + player.username)

    def __event_trader_open(self):
        self.__send_message("!trader_open")

    def __event_trader_close(self):
        self.__send_message("!trader_close")

    def __event_victory(self):
        self.__send_message("!victory")

    def __event_failure(self):
        self.__send_message("!failure")
