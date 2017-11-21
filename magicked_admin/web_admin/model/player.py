
class Player(object):
    def __init__(self, username, perk):
        self.kills = 0
        self.dosh = 0
        self.health = 0

        self.username = username
        self.perk = perk
        self.ping = 0
