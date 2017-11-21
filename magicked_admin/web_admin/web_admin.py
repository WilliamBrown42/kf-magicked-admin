from itertools import groupby
from lxml import html
import logging

from utils.text import str_to_bool
from utils.geolocation import get_country
from web_admin.model.game import Game
from web_admin.model.player import Player

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class WebAdmin(object):
    def __init__(self, web_interface, game_password=None):

        self.__web_interface = web_interface

        self.__general_settings = self.general_settings()
        self.__motd_settings = self.motd_settings()

        self.game = Game()
        self.players = []

        self.__game_password = game_password

        self.refresh_server_info()

    def general_settings(self):
        response = self.__web_interface.get_general_settings()
        general_settings_tree = html.fromstring(response.content)

        settings_names = general_settings_tree.xpath('//input/@name')
        settings_vals = general_settings_tree.xpath('//input/@value')

        radio_settings_names = general_settings_tree.xpath(
            '//input[@checked="checked"]/@name'
        )
        radio_settings_vals = general_settings_tree.xpath(
            '//input[@checked="checked"]/@value'
        )

        length_val = general_settings_tree.xpath(
            '//select[@id="settings_GameLength"]' +
            '//option[@selected="selected"]/@value'
        )[0]
        difficulty_val = general_settings_tree.xpath(
            '//input[@name="settings_GameDifficulty_raw"]/@value'
        )[0]

        settings = {'settings_GameLength': length_val,
                    'settings_GameDifficulty': difficulty_val,
                    'action': 'save'}

        for i in range(0, len(settings_names)):
            settings[settings_names[i]] = settings_vals[i]

        for i in range(0, len(radio_settings_names)):
            settings[radio_settings_names[i]] = radio_settings_vals[i]

        return settings

    def motd_settings(self):
        response = self.__web_interface.get_motd_settings()
        motd_tree = html.fromstring(response.content)

        banner_link = motd_tree.xpath('//input[@name="BannerLink"]/@value')[0]
        web_link = motd_tree.xpath('//input[@name="WebLink"]/@value')[0]

        return {
            'BannerLink': banner_link,
            'ClanMotto': '',
            'ClanMottoColor': '#FF0000',
            'ServerMOTDColor': '#FF0000',
            'WebLink': web_link,
            'WebLinkColor': '#FF0000',
            'liveAdjust': '1',
            'action': 'save'
        }

    def refresh_server_info(self):
        self.players = []

        response = self.__web_interface.get_server_info()
        info_tree = html.fromstring(response.content)
        self.__update_game(info_tree)
        self.__update_players(info_tree)

    def __update_players(self, info_tree):
        odds = info_tree.xpath('//tr[@class="odd"]//td/text()')
        evens = info_tree.xpath('//tr[@class="even"]//td/text()')
        player_rows = odds + evens

        player_rows = [list(group) for k, group in
                       groupby(player_rows, lambda x: x == "\xa0") if not k]

        for player_row in player_rows:
            if len(player_row) < 6:
                # Player hasn't readied up yet
                continue
            if len(player_row) < 7:
                # Player is dead
                username, perk, dosh = player_row[:3]
                health = 0
                kills, ping = player_row[3:5]
            else:
                # Player is ready and alive
                username, perk, dosh, health, kills, ping \
                    = player_row[:6]

            player = Player(username, perk)
            player.kills = int(kills)
            player.health = int(health)
            player.dosh = int(dosh)
            player.ping = int(ping)

            self.players.append(player)

    def __update_game(self, info_tree):
        zed_status_pattern = "//dd[@class=\"gs_wave\"]/text()"
        zeds_dead, zeds_total = \
            info_tree.xpath(zed_status_pattern)[0].split("/")
        zeds_dead, zeds_total = int(zeds_dead), int(zeds_total)

        if zeds_dead == zeds_total and zeds_total > 1:
            self.game.trader_open = True
        else:
            self.game.trader_open = False

        self.game.zeds_total = zeds_total
        self.game.zeds_dead = zeds_dead

        dds = info_tree.xpath('//dd/text()')
        game_type = info_tree.xpath('//dl//dd/@title')[0]
        map_title = info_tree.xpath('//dl//dd/@title')[1]
        map_name = dds[0]
        wave, length = dds[7].split("/")
        difficulty = dds[8]

        self.game.map_title = map_title
        self.game.map_name = map_name
        self.game.wave = wave
        self.game.length = length
        self.game.difficulty = difficulty
        self.game.game_type = game_type

    def __save_general_settings(self):
        self.__web_interface.post_general_settings(
            self.__general_settings
        )

    def set_general_setting(self, setting, value):
        self.__general_settings[setting] = value
        self.__save_general_settings()

    def set_game_password(self, password):
        payload = {
            'action': 'gamepassword',
            'gamepw1': password,
            'gamepw2': password
        }
        self.__web_interface.post_passwords(payload)

    def has_game_password(self):
        response = self.__web_interface.get_passwords
        passwords_tree = html.fromstring(response.content)

        password_state_pattern = "//p[starts-with(text(),\"Game password\")]" \
                                 "//em/text()'"
        password_state = passwords_tree.xpath(password_state_pattern)[0]
        return str_to_bool(password_state)

    def toggle_game_password(self):
        if not self.__game_password:
            return False

        if self.has_game_password():
            self.set_game_password("")
            return False
        else:
            self.set_game_password(self.__game_password)
            return True

    def set_length(self, length):
        self.set_general_setting("settings_GameLength", length)

    def set_difficulty(self, difficulty):
        self.set_general_setting("settings_GameDifficulty", difficulty)

    def set_max_players(self, players):
        self.set_general_setting("settings_MaxPlayers", str(players))

    def toggle_map_voting(self):
        if self.__general_settings["settings_bDisableMapVote"] == "1":
            self.set_general_setting("settings_bDisableMapVote", "0")
            return False
        else:
            self.set_general_setting("settings_bDisableMapVote", "1")
            return True

    def set_server_name(self, name):
        self.set_general_setting("settings_ServerName", name)

    def set_map(self, new_map):
        payload = {
            "gametype": self.game.game_type,
            "map": new_map,
            "mutatorGroupCount": "0",
            "urlextra": "?MaxPlayers=" + self.game.max_players,
            "action": "change"
        }
        self.__web_interface.post_map(payload)

    def restart_map(self):
        self.set_map(self.game.map_title)

    def set_game_type(self, game_type):
        self.game.game_type = game_type
        self.restart_map()

    def activate_map_cycle(self, index):
        payload = {
            "maplistidx": str(index),
            "mapcycle": "KF-Default",
            "activate": "activate"
        }
        self.__web_interface.post_map_cycle(payload)

    def set_map_cycle(self, index, maplist):
        payload = {
            "maplistidx": str(index),
            "mapcycle": maplist,
            "action": "save"
        }
        self.__web_interface.post_map_cycle(payload)

    def set_motd(self, motd):
        self.__motd_settings["ServerMOTD"] = motd\
            .encode("iso-8859-1", "ignore")
        self.__web_interface.post_motd(self.__motd_settings)
        # Setting the MOTD resets changes to general settings
        self.__save_general_settings()

    def set_banner(self, banner_link):
        self.__motd_settings["BannerLink"] = banner_link
        self.__web_interface.post_motd(self.__motd_settings)

    def set_web_link(self, web_link):
        self.__motd_settings["WebLink"] = web_link
        self.__web_interface.post_motd(self.__motd_settings)

    def get_player_details(self, username):
        response = self.__web_interface.get_players()
        player_tree = html.fromstring(response.content)

        odds = player_tree.xpath('//tr[@class="odd"]//td/text()')
        evens = player_tree.xpath('//tr[@class="even"]//td/text()')

        player_rows = odds + evens

        for player in player_rows:
            if player[1] == username:
                ip = player[3]
                steam_id = player[5]
                country, country_code = get_country(ip)
                return {
                    'steam_id': steam_id,
                    'ip': ip,
                    'country': country,
                    'country_code': country_code
                }

        logger.warning("Country find player details for: {}".format(username))
        return {
                    'steam_id': "00000000000000000",
                    'ip': "0.0.0.0",
                    'country': "Unknown",
                    'country_code': "??"
                }
