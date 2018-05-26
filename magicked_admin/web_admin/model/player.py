class Player(object):
    def __init__(self, steam_id, country_code, ip, username):
        self.steam_id = steam_id
        self.id = "000"
        self.key = "000_0000000000000000_000.0000"
        self.country = "Unknown"
        self.country_code = country_code
        self.ip = ip
        self.username = username

        self.perk = "None"
        self.perk_level = 99
        self.ping = 0
        self.kills = 0
        self.dosh = 0
        self.health = 0

        self.wave_kills = 0
        self.wave_dosh = 0

        self.dosh_earned = 0
        self.dosh_spent = 0
