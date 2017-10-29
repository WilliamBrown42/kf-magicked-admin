import requests

from hashlib import sha1

from lxml import html

class Server():
   
    def __init__(self, name, address, username, password):
        self.name = name
        self.address = address
        self.username = username
        self.password_hash = "$sha1$" + \
            sha1(password.encode("iso-8859-1","ignore") + \
                username.encode("iso-8859-1","ignore")) \
            .hexdigest()

        self.session = self.new_session()
        self.motd = self.load_motd()

        self.game = {
            'players_max': 6,
            'map': 'kf-default',
            'round': 0,
            'length': 7,
            'difficulty':'normal'
        }

        self.players = {}

    def __str__(self):
        return "I'm " + self.name + " at " + self.address +\
            ".\nThe admin is " + self.username + ". The game is currently:\n\t" + str(self.game)

    def new_session(self):
        login_url = "http://" + self.address + "/ServerAdmin/"
        login_payload = {
            'password_hash': self.password_hash,
            'username': self.username,
            'password': '',
            'remember': '-1'
        }

        s = requests.Session()

        login_page_response = s.get(login_url)
        login_page_tree = html.fromstring(login_page_response.content)
        
        token = login_page_tree.xpath('//input[@name="token"]/@value')[0]
        login_payload.update({'token':token})

        s.post(login_url, data=login_payload)
        
        return s
        
    def load_motd(self):
        motd_f = open(self.name + ".motd")
        motd = motd_f.read()
        motd_f.close()

        return motd.encode("iso-8859-1", "ignore")
