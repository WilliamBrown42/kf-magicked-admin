from os import path
import threading

from utils.text import millify
from utils.text import trim_string


class MotdUpdater(threading.Thread):

    def __init__(self, web_admin, data_logger, database):
        self.web_admin = web_admin
        self.database = database
        self.data_logger = data_logger

        self.time_interval = 5 * 60
        self.motd = self.load_motd()

        self.exit_flag = threading.Event()

        threading.Thread.__init__(self)
    
    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            self.data_logger.write_all_players()

            motd = self.render_motd(self.motd)

            self.web_admin.set_motd(motd)

    def load_motd(self):
        if not path.exists(self.server.name + ".motd"):
            print("WARNING: No motd file for " + self.server.name)
            return ""
 
        motd_f = open(self.server.name + ".motd")
        motd = motd_f.read()
        motd_f.close()
        return motd

    def render_motd(self, src_motd):
        scores = self.server.database.top_kills()

        for player in scores:
            name = player[0].replace("<","&lt;")
            name = trim_string(name, 12)
            score = player[1]

            src_motd = src_motd.replace("%PLR", name, 1)
            src_motd = src_motd.replace("%SCR", millify(score), 1)
        
        return src_motd

    def terminate(self):
        self.exit_flag.set()
