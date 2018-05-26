import requests
from hashlib import sha1
from lxml import html
import logging
import time

'''DIFF_NORM = "0.0000"
DIFF_HARD = "1.0000"
DIFF_SUI = "2.0000"
DIFF_HOE = "4.0000"

LEN_SHORT = "0"
LEN_NORM = "1"
LEN_LONG = "2"

MODE_SURVIVAL = "KFGameContent.KFGameInfo_Survival"
MODE_WEEKLY = "KFGameContent.KFGameInfo_WeeklySurvival"
MODE_SURVIVAL_VS = "KFGameContent.KFGameInfo_VersusSurvival"'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class WebInterface(object):
    def __init__(self, address, username, password, multi_admin=False):
        # validate address here, rise if bad
        self.__address = address
        self.__username = username
        if multi_admin:
            self.__password_hash = "$sha1$" + \
                 sha1(
                     password.encode("iso-8859-1", "ignore") +
                     username.encode("iso-8859-1", "ignore")
                 ).hexdigest()
        else:
            logger.info("Multi-admin disabled on {}, passwords will not be "
                        "hashed.".format(address))
            self.__password_hash = password

        self.__urls = {
            'login': 'http://{0}/ServerAdmin/'
                .format(address),
            'chat': 'http://{0}/ServerAdmin/current/chat+data'
                .format(address),
            'info': 'http://{0}/ServerAdmin/current/info'
                .format(address),
            'map': 'http://{0}/ServerAdmin/current/change'
                .format(address),
            'players': 'http://{0}/ServerAdmin/current/players'
                .format(address),
            'passwords': 'http://{0}/ServerAdmin/policy/passwords'
                .format(address),
            'bans': 'http://{0}/ServerAdmin/policy/bans'
                .format(address),
            'general_settings': 'http://{0}/ServerAdmin/settings/general'
                .format(address),
            'game_type': 'http://{0}/ServerAdmin/settings/gametypes'
                .format(address),
            'map_cycle': 'http://{0}/ServerAdmin/settings/maplist'
                .format(address),
            'welcome': 'http://{0}/ServerAdmin/settings/welcome'
                .format(address),
            'console': 'http://{0}/ServerAdmin/console'
                .format(address)
        }

        self.__retry_interval = 6
        self.__retry_interval_urgent = 3
        self.__timeout = 5

        self.__session = self.__new_session()

        self.__chat_session = self.__new_session()

    def __get(self, session, url, urgent=False):
        retry_interval = self.__retry_interval_urgent if urgent \
            else self.__retry_interval

        while True:
            try:
                response = session.get(url, timeout=self.__timeout)
                return response
            except requests.exceptions.HTTPError:
                logger.info("HTTPError getting {}. Retrying in {}"
                            .format(url, retry_interval))
            except requests.exceptions.ConnectionError:
                logger.info("ConnectionError getting {}. Retrying in {}"
                            .format(url, retry_interval))
            except requests.exceptions.Timeout:
                logger.info("Timeout getting {}. Retrying in {}"
                            .format(url, retry_interval))
            except requests.exceptions.RequestException as err:
                logger.warning("None-specific RequestException getting {}, "
                               "{}. Retrying in {}"
                               .format(url, str(err), retry_interval))

            time.sleep(retry_interval)

    def __post(self, session, url, payload, urgent=False):
        retry_interval = self.__retry_interval_urgent if urgent \
            else self.__retry_interval

        while True:
            try:
                response = session.post(
                    url, payload,
                    timeout=self.__timeout
                )
                return response
            except requests.exceptions.HTTPError:
                logger.info("HTTPError posting {}. Retrying in {}"
                            .format(url, retry_interval))
            except requests.exceptions.ConnectionError:
                logger.info("ConnectionError posting {}. Retrying in {}"
                            .format(url, retry_interval))
            except requests.exceptions.Timeout:
                logger.info("Timeout posting {}. Retrying in {}"
                            .format(url, retry_interval))
            except requests.exceptions.RequestException as err:
                logger.warning("None-specific RequestException posting {}, "
                               "{}. Retrying in {}"
                               .format(url, str(err), retry_interval))

            time.sleep(retry_interval)

    def __new_session(self):
        login_payload = {
            'password_hash': self.__password_hash,
            'username': self.__username,
            'password': '',
            'remember': '-1'
        }

        session = requests.Session()
        login_page_response = self.__get(session, self.__urls['login'])

        login_page_tree = html.fromstring(login_page_response.content)
        token_pattern = "//input[@name='token']/@value"
        token = login_page_tree.xpath(token_pattern)[0]
        login_payload.update({'token': token})

        self.__post(session, self.__urls['login'], login_payload)

        return session

    def get_new_messages(self, urgent=False):
        payload = {
            'ajax': '1'
        }

        return self.__post(
            self.__chat_session,
            self.__urls['chat'],
            payload,
            urgent
        )

    def post_message(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['chat'],
            payload,
            urgent
        )

    def get_server_info(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['info'],
            urgent
        )

    def get_map(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['map'],
            urgent
        )

    def post_map(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['map'],
            payload,
            urgent
        )

    def get_players(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['players'],
            urgent
        )

    def get_passwords(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['passwords'],
            urgent
        )

    def post_passwords(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['passwords'],
            payload,
            urgent
        )

    def get_bans(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['bans'],
            urgent
        )

    def post_bans(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['bans'],
            payload,
            urgent
        )

    def get_general_settings(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['general_settings'],
            urgent
        )

    def post_general_settings(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['general_settings'],
            payload,
            urgent
        )

    def get_game_type(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['game_type'],
            urgent
        )

    def post_game_type(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['game_type'],
            payload,
            urgent
        )

    def get_map_cycle(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['map_cycle'],
            urgent
        )

    def post_map_cycle(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['map_cycle'],
            payload,
            urgent
        )

    def get_welcome(self, urgent=False):
        return self.__get(
            self.__session,
            self.__urls['welcome'],
            urgent
        )

    def post_welcome(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['welcome'],
            payload,
            urgent
        )

    def post_command(self, payload, urgent=False):
        return self.__post(
            self.__session,
            self.__urls['console'],
            payload,
            urgent
        )

    def get_payload_general_settings(self):
        response = self.get_general_settings()
        general_settings_tree = html.fromstring(response.content)

        settings_names = general_settings_tree.xpath('//input/@name')
        settings_vals = general_settings_tree.xpath('//input/@value')

        radio_settings_names = general_settings_tree.xpath(
            '//input[@checked="checked"]/@name'
        )
        radio_settings_vals = general_settings_tree.xpath(
            '//input[@checked="checked"]/@value'
        )

        # Line 310 breaks in refactor, index error, likely old fixes will work
        length_val = general_settings_tree.xpath(
            '//select[@id="settings_GameLength"]' +
            '//option[@selected="selected"]/@value'
        )[0]
        difficulty_val = general_settings_tree.xpath(
            '//input[@name="settings_GameDifficulty_raw"]/@value'
        )[0]

        settings = {'settings_GameLength': length_val,
                    'settings_GameDifficulty': difficulty_val,
                    'action': 'save'}

        for i in range(0, len(settings_names)):
            settings[settings_names[i]] = settings_vals[i]

        for i in range(0, len(radio_settings_names)):
            settings[radio_settings_names[i]] = radio_settings_vals[i]

        return settings

    def get_payload_motd_settings(self):
        response = self.get_welcome()
        motd_tree = html.fromstring(response.content)

        banner_link = motd_tree.xpath('//input[@name="BannerLink"]/@value')[0]
        web_link = motd_tree.xpath('//input[@name="WebLink"]/@value')[0]

        return {
            'BannerLink': banner_link,
            'ClanMotto': '',
            'ClanMottoColor': '#FF0000',
            'ServerMOTDColor': '#FF0000',
            'WebLink': web_link,
            'WebLinkColor': '#FF0000',
            'liveAdjust': '1',
            'action': 'save'
        }

    def get_payload_map_settings(self):
        response = self.get_map()
        map_tree = html.fromstring(response.content)

        game_type_pattern = "//select[@id=\"gametype\"]" \
                            "//option[@selected=\"selected\"]/@value"
        map_pattern = "//select[@id=\"map\"]" \
                      "//option[@selected=\"selected\"]/@value"
        url_extra_pattern = "//input[@id=\"urlextra\"]/@value"
        mutator_count_pattern = "//input[@name=\"mutatorGroupCount\"]/@value"

        game_type = map_tree.xpath(game_type_pattern)[0]
        map_name = map_tree.xpath(map_pattern)[0]
        url_extra = map_tree.xpath(url_extra_pattern)[0]
        mutator_count = map_tree.xpath(mutator_count_pattern)[0]

        return {
            "gametype": game_type,
            "map": map_name,
            "mutatorGroupCount": mutator_count,
            "urlextra": url_extra,
            "action": "change"
        }
