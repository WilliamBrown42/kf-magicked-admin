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

    def load_player(self, player):
        player.total_kills = self.queries.player_kills(player.username)
        player.total_dosh = self.queries.player_dosh(player.username)
        player.total_deaths = self.queries.player_deaths(player.username)
        player.total_dosh_spent = self.queries.player_dosh_spent(player.username)
        player.total_logins = self.queries.player_logins(player.username)
        player.total_health_lost = self.queries.player_health_lost(player.username)
        player.total_time = self.queries.player_time(player.username)

    def save_player(self, player, final=False):
        self.cur.execute("INSERT OR IGNORE INTO players (username) VALUES (?)", \
                         (player.username,))

        self.cur.execute(
            "UPDATE players SET dosh_spent = ? WHERE username = ?", \
            (player.total_dosh_spent, player.username))
        self.cur.execute("UPDATE players SET dosh = ? WHERE username = ?", \
                         (player.total_dosh, player.username))
        self.cur.execute("UPDATE players SET kills = ? WHERE username = ?", \
                         (player.total_kills, player.username))
        self.cur.execute("UPDATE players SET deaths = ? WHERE username = ?", \
                         (player.total_deaths, player.username))
        self.cur.execute(
            "UPDATE players SET health_lost = ? WHERE username = ?", \
            (player.total_health_lost, player.username))
        self.cur.execute("UPDATE players SET logins = ? WHERE username = ?", \
                         (player.total_logins, player.username))

        if final:
            now = datetime.datetime.now()
            elapsed_time = now - player.session_start
            seconds = elapsed_time.total_seconds()
            new_time = player.total_time + seconds

            self.cur.execute(
                "UPDATE players SET time_online = ? WHERE username = ?", \
                (new_time, player.username))

        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()

