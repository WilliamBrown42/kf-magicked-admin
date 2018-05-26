from chatbot.commands.command import Command
from utils.time import seconds_to_hhmmss
from utils.text import millify

import datetime


<<<<<<< HEAD
class CommandPlayers(Command):  
    def __init__(self, operator_list, data_logger, admin=True):
        Command.__init__(self, operator_list, admin)

        self.data_logger = data_logger
        
=======
class CommandPlayers(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

>>>>>>> master
    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        message = ""

        for player in self.data_logger.players:
            message += str(player) + " \n"
        message = message.strip()
        return message


class CommandGame(Command):
<<<<<<< HEAD
    def __init__(self, operator_list, data_logger, admin=True):
        Command.__init__(self, operator_list, admin)

        self.data_logger = data_logger
=======
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return str(self.data_logger.game)


class CommandGameMap(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return str(self.server.game.game_map)

class CommandHighWave(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return "{} is the highest wave reached on this map."\
            .format(self.server.game.game_map.highest_wave)

class CommandHelp(Command):
<<<<<<< HEAD
    def __init__(self, operator_list, help_text, admin=True):
        Command.__init__(self, operator_list, admin)

        self.help_text = help_text
=======
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
<<<<<<< HEAD

        return self.help_text


class CommandInfo(Command):
    def __init__(self, operator_list, admin=True):
        Command.__init__(self, operator_list, admin)
=======
        return "Player commands:\n !me, !dosh, !kills, !server_dosh," \
               " !server_kills, !top_dosh, !top_kills, !stats, !info"


class CommandInfo(Command):
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        return "I'm a bot for ranked Killing Floor 2 servers. Visit:\n" \
            "github.com/th3-z/kf-magicked-admin/\n" + \
            "for information, source code, and credits."


class CommandMe(Command):
<<<<<<< HEAD
    def __init__(self, operator_list, data_logger, admin=True):
        Command.__init__(self, operator_list, admin)

        self.stats_command = CommandStats(operator_list, data_logger,
                                          admin=False)
=======
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

<<<<<<< HEAD
        return self.stats_command.execute(
            "server", ["stats", username], admin=True
        )

=======
        stats_command = CommandStats(self.server, admin_only=False)
        return stats_command.execute("server", ["stats", username], admin=True)
>>>>>>> master


class CommandStats(Command):
<<<<<<< HEAD
    def __init__(self, operator_list, data_logger, admin=True):
        Command.__init__(self, operator_list, admin)

        self.data_logger = data_logger
=======
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "Missing argument (username)"
<<<<<<< HEAD
            
        self.data_logger.write_players()
        requested_username = " ".join(args[1:])
        
        player = self.data_logger.get_player(requested_username)
=======

        self.server.write_all_players()
        requested_username = " ".join(args[1:])

        player = self.server.get_player(requested_username)
>>>>>>> master
        if player:
            now = datetime.datetime.now()
            elapsed_time = now - player.session_start
            session_time = elapsed_time.total_seconds()
        else:
            session_time = 0
<<<<<<< HEAD
            # TODO load player by steam id, datalogger method
            #player = Player(requested_username, "no-perk")
            #self.server.database.load_player(player)
            
=======
            player = Player(requested_username, "no-perk")
            self.server.database.load_player(player)

>>>>>>> master
        time = seconds_to_hhmmss(
            player.total_time + session_time
        )
        message = "Stats for {}:\n".format(player.username) +\
                  "Total play time: {} ({} sessions)\n"\
                      .format(time, player.total_logins) +\
                  "Total deaths: {}\n".format(player.total_deaths) +\
                  "Total kills: {}\n".format(millify(player.total_kills)) +\
                  "Total dosh earned: {}\n"\
                      .format(millify(player.total_dosh)) +\
                  "Dosh this game: {}".format(millify(player.game_dosh))

        return message
