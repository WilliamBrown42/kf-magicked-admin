import sqlite3
import datetime
from os import path

from database.queries import DatabaseQueries


class DatabaseController(object):
    def __init__(self, name):
        self.sqlite_db_file = name + "_db" + ".sqlite"

        if not path.exists(self.sqlite_db_file):
            self.build_schema()
        self.conn = sqlite3.connect(self.sqlite_db_file,
                                    check_same_thread=False)
        self.cur = self.conn.cursor()

        self.queries = DatabaseQueries(self.cur)

        print("INFO: Database for " + name + " initialised")

    def build_schema(self):
        print("INFO: Building fresh schema...")

        conn = sqlite3.connect(self.sqlite_db_file)
        cur = conn.cursor()

        with open('database/server_schema.sql') as schema_file:
            cur.executescript(schema_file.read())

        conn.commit()
        conn.close()

    '''def load_player(self, sid):
        player.total_kills = self.queries.player_kills(player.username)
        player.total_dosh = self.queries.player_dosh(player.username)
        player.total_deaths = self.queries.player_deaths(player.username)
        player.total_dosh_spent = self.queries.player_dosh_spent(player.username)
        player.total_logins = self.queries.player_logins(player.username)
        player.total_health_lost = self.queries.player_health_lost(player.username)
        player.total_time = self.queries.player_time(player.username)'''

    def open_session(self, player, game):
        # Insert new player, update country information
        self.cur.execute(
            "INSERT OR IGNORE INTO player (steam_id) VALUES (?)",
            (player.steam_id,))
        self.cur.execute(
            "UPDATE player SET country_code = ? WHERE steam_id = ?",
            (player.country_code, player.steam_id))
        self.cur.execute(
            "UPDATE player SET username = ? WHERE steam_id = ?",
            (player.username, player.steam_id))

        timestamp = datetime.datetime.now().isoformat()
        self.cur.execute(
            "INSERT INTO session (steam_id, date_start) VALUES (?)",
            (player.steam_id, timestamp))
        session_id = self.cur.lastrowid

        self.cur.execute(
            "INSERT INTO game_session (session_id, game_id) VALUES (?)",
            (session_id, game.id))

        self.conn.commit()
        return session_id

    def write_session(self, player):
        self.cur.execute(
            "UPDATE session SET kills = ? WHERE steam_id = ?",
            (player.kills, player.steam_id))

        self.cur.execute(
            "UPDATE session SET deaths = ? WHERE steam_id = ?",
            (player.deaths, player.steam_id))

        self.cur.execute(
            "UPDATE session SET dosh_earned = ? WHERE steam_id = ?",
            (player.dosh_earned, player.steam_id))

        self.cur.execute(
            "UPDATE session SET dosh_spent = ? WHERE steam_id = ?",
            (player.dosh_spent, player.steam_id))

    def close_session(self, player):
        self.write_session(player)

        self.cur.execute(
            "UPDATE session SET date_end = ? WHERE steam_id = ?",
            (datetime.datetime.now(), player.steam_id))

        self.conn.commit()

    def open_game(self, game):
        timestamp = datetime.datetime.now().isoformat()
        self.cur.execute(
            "INSERT INTO game (map_id, game_mode, date_start) VALUES (?)",
            (game.map_id, game.game_mode, timestamp))

        game_id = self.cur.lastrowid

        self.conn.commit()
        return game_id

    def close_game(self, game):
        timestamp = datetime.datetime.now().isoformat()
        self.cur.execute(
            "UPDATE game SET date_end = ? WHERE game_id = ?",
            (timestamp, game.game_id))

    def close(self):
        self.conn.commit()
        self.conn.close()
