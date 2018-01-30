from chatbot.commands.command import Command
from utils.text import trim_string, millify


class CommandKills(Command):
    def __init__(self, operator_list, data_logger, admin=True):
        Command.__init__(self, operator_list, admin)

        self.data_logger = data_logger
        
    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        player = self.data_logger.get_player(username)
        if player:
            return "You've killed a total of " + str(player.total_kills) + \
                    " ZEDs, and " + str(player.kills) + " this game."
        else:
            # TODO return the number of kills named player has total
            return "Player not in game."


class CommandDosh(Command):
    def __init__(self, operator_list, data_logger, admin=True):
        Command.__init__(self, operator_list, admin)

        self.data_logger = data_logger
        
    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        player = self.data_logger.get_player(username)
        if player:
            return ("You've earned £" + str(player.total_dosh) +
                    " in total, and £" + str(player.game_dosh) +
                    " this game.").encode("iso-8859-1", "ignore")
        else:
            # TODO return offline player's total dosh
            return "Player not in game."


class CommandTopKills(Command):
    def __init__(self, operator_list, data_logger, queries, admin=True):
        Command.__init__(self, operator_list, admin)

        self.data_logger = data_logger
        self.queries = queries

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        self.data_logger.write_players()
        killers = self.queries.top_kills()
        if len(killers) < 5:
            return "Not enough data."
        
        return "\n\nTop 5 players by kills:\n" + \
            "\t"+str(millify(killers[0][1])) + "\t-\t" + trim_string(killers[0][0],20) + "\n" + \
            "\t"+str(millify(killers[1][1])) + "\t-\t" + trim_string(killers[1][0],20) + "\n" + \
            "\t"+str(millify(killers[2][1])) + "\t-\t" + trim_string(killers[2][0],20) + "\n" + \
            "\t"+str(millify(killers[3][1])) + "\t-\t" + trim_string(killers[3][0],20) + "\n" + \
            "\t"+str(millify(killers[4][1])) + "\t-\t" + trim_string(killers[4][0],20)


class CommandTopDosh(Command):
    def __init__(self, operator_list, data_logger, queries, admin=True):
        Command.__init__(self, operator_list, admin)

        self.data_logger = data_logger
        self.queries = queries

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        self.data_logger.write_players()
        doshers = self.queries.top_dosh()
        if len(doshers) < 5:
            return "Not enough data."
            
        message = "\n\nTop 5 players by earnings:\n" + \
            "\t£"+str(millify(doshers[0][1])) + "\t-\t" + trim_string(doshers[0][0],20) + "\n" + \
            "\t£"+str(millify(doshers[1][1])) + "\t-\t" + trim_string(doshers[1][0],20) + "\n" + \
            "\t£"+str(millify(doshers[2][1])) + "\t-\t" + trim_string(doshers[2][0],20) + "\n" + \
            "\t£"+str(millify(doshers[3][1])) + "\t-\t" + trim_string(doshers[3][0],20) + "\n" + \
            "\t£"+str(millify(doshers[4][1])) + "\t-\t" + trim_string(doshers[4][0],20)
        return message.encode("iso-8859-1","ignore")
