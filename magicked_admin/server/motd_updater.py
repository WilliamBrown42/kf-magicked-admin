from os import path
import threading
from random import randint

from utils.text import millify
from utils.text import trim_string

SCORE_TYPE_KILLS = "kills"
SCORE_TYPE_DOSH = "dosh earned"
SCORE_TYPE_RANDOM = "random"
SCORE_TYPE_TIME = "time played"


class MotdUpdater(threading.Thread):

    def __init__(self, web_admin, motd_file, database,
                 score_type=SCORE_TYPE_RANDOM):
        self.web_admin = web_admin
        self.database = database

        self.time_interval = 5 * 60
        self.motd = self.load_motd(motd_file)
        self.score_type = score_type

        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
    
    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            self.data_logger.write_all_players()

            motd = self.render_motd(self.motd)

            self.web_admin.set_motd(motd)

    @staticmethod
    def load_motd(motd_file):
        if not path.exists(motd_file):
            print("WARNING: No such motd file: " + motd_file)
            return ""
 
        motd_f = open(motd_file)
        motd = motd_f.read()
        motd_f.close()
        return motd

    def render_motd(self, src_motd):
        scores = self.server.database.top_kills()

        score_type = self.score_type
        if score_type == SCORE_TYPE_RANDOM:
            score_type = [
                SCORE_TYPE_KILLS,
                SCORE_TYPE_DOSH,
                SCORE_TYPE_TIME
            ][randint() % 3]

        src_motd = src_motd.replace("%TYP", score_type, 1)

        for player in scores:
            name = player[0].replace("<","&lt;")
            name = trim_string(name, 12)
            score = player[1]

            src_motd = src_motd.replace("%PLR", name, 1)
            src_motd = src_motd.replace("%SCR", millify(score), 1)
        
        return src_motd

    def terminate(self):
        self.exit_flag.set()
