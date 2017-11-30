import threading
import random

DEFAULT_MAPS = [
    "KF-BioticsLab", "KF-BlackForest", "KF-BurningParis",
    "KF-Catacombs", "KF-ContainmentStation", "KF-EvacuationPoint",
    "KF-Farmhouse", "KF-HostileGrounds", "KF-InfernalRealm",
    "KF-Nightmare", "KF-Nuked", "KF-Outpost",
    "KF-Prison", "KF-TragicKingdom", "KF-TheDescent",
    "KF-VolterManor", "KF-ZedLanding"
]


class Watchdog(threading.Thread):

    def __init__(self, web_admin, data_logger):
        # 5 minutes
        self.time_interval = 240 * 60
        self.exit_flag = threading.Event()
        self.web_admin = web_admin
        self.data_logger = data_logger

        self.last_map = ""
        
        threading.Thread.__init__(self)

    def run(self):
        while not self.exit_flag.wait(self.time_interval):
            if self.last_map == self.data_logger.game.map.title and \
                            len(self.data_logger.players) < 1:
                print("INFO: Watchdog found a stuck map " +
                      self.data_logger.game.map.title)
                self.web_admin.change_map(random.choice(DEFAULT_MAPS))
                
            self.last_map = self.data_logger.game.map.title

    def terminate(self):
        self.exit_flag.set()

