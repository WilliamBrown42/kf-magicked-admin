
class Player(object):
    def __init__(self, steam_id, country_code, ip, username):
        self.steam_id = steam_id
        self.country_code = country_code
        self.ip = ip
        self.username = username

        self.perk = "None"
        self.ping = 0
        self.kills = 0
        self.dosh = 0
        self.health = 0

        self.wave_kills = 0
        self.wave_dosh = 0

        self.dosh_earned = 0
        self.dosh_spent = 0
