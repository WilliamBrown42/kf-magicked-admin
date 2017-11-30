import datetime


class Map(object):
    def __init__(self):
        self.title = ""
        self.name = ""

        self.plays = 0
        self.votes = 0

        self.last_played = datetime.datetime.now()
