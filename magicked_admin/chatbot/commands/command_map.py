from chatbot.commands.player_commands import *
from chatbot.commands.info_commands import *
from chatbot.commands.server_commands import *
#from chatbot.commands.event_commands import *

<<<<<<< HEAD

def build_command_map(server, chatbot, operator_commands):
    #wave_event_manager = CommandOnWaveManager(server, chatbot)
    #trader_event_manager = CommandOnTraderManager(server, chatbot)
    #time_event_manager = CommandOnTimeManager(server, chatbot)

    command_map = {
        '''''stop_wc': wave_event_manager,
        'start_wc': wave_event_manager,
        'new_wave': wave_event_manager,
        'start_tc': time_event_manager,
        'stop_tc': time_event_manager,
        'start_trc': trader_event_manager,
        'stop_trc': trader_event_manager,
        't_close': trader_event_manager,
        't_open': trader_event_manager,'''
        
        'say': CommandSay(server.operators,
                          admin='say' in operator_commands),
        'restart': CommandRestart(server.operators, server.web_admin,
                                  admin='restart' in operator_commands),
        'toggle_pass': CommandTogglePassword(server.operators, server.web_admin,
                                             admin=
                                             'toggle_pass' in operator_commands),
        'silent': CommandSilent(server.operators, chatbot,
                                admin='silent' in operator_commands),
        'length': CommandLength(server.operators, server.web_admin,
                                admin='length' in operator_commands),
        'difficulty': CommandDifficulty(server.operators, server.web_admin,
                                        admin='difficulty' in operator_commands),
        'players': CommandPlayers(server.operators, server.data_logger,
                                  admin='players' in operator_commands),
        'game': CommandGame(server.operators, server.data_logger,
                            admin='game' in operator_commands),
        'help': CommandHelp(server.operators, server.help_text,
                            admin='help' in operator_commands),
        'info': CommandInfo(server.operators,
                            admin='info' in operator_commands),
        'kills': CommandKills(server.operators, server.data_logger,
                              admin='kills' in operator_commands),
        'dosh': CommandDosh(server.operators, server.data_logger,
                            admin='dosh' in operator_commands),
        'top_kills': CommandTopKills(server.operators, server.data_logger,
                                     server.database_queries,
                                     admin='top_kills' in operator_commands),
        'top_dosh': CommandTopDosh(server.operators, server.data_logger,
                                   server.database_queries,
                                   admin='top_dosh' in operator_commands),
        'me': CommandMe(server.operators, server.data_logger,
                        admin='me' in operator_commands),
        'stats': CommandStats(server.operators, server.data_logger,
                              admin='stats' in operator_commands)
    }

    return command_map

=======

class CommandMap:
    def __init__(self, server, chatbot):
        self.server = server
        self.chatbot = chatbot
        self.command_map = self.generate_map()

    def generate_map(self):
        """
        Generates the command mapping (key/value pairs) that are used by the (chat bot was it?)
        """
        wave_event_manager = CommandOnWaveManager(self.server, self.chatbot)
        trader_event_manager = CommandOnTraderManager(self.server, self.chatbot)
        time_event_manager = CommandOnTimeManager(self.server, self.chatbot)
        greeter = CommandGreeter(self.server)

        command_map = {
            'new_game': greeter,
            'player_join': greeter,
            'stop_wc': wave_event_manager,
            'start_wc': wave_event_manager,
            'new_wave': wave_event_manager,
            'start_tc': time_event_manager,
            'stop_tc': time_event_manager,
            'start_trc': trader_event_manager,
            'stop_trc': trader_event_manager,
            't_close': trader_event_manager,
            't_open': trader_event_manager,
            'enforce_levels': CommandEnforceLevels(self.server),
            'record_wave': CommandHighWave(self.server, admin_only=False),
            'say': CommandSay(self.server),
            'restart': CommandRestart(self.server),
            'load_map': CommandLoadMap(self.server),
            'pass': CommandEnablePassword(self.server),
            'pass_off': commandDisablePassword(self.server),
            'silent': CommandSilent(self.server, self.chatbot),
            'run': CommandRun(self.server, self.chatbot),
            'length': CommandLength(self.server),
            'difficulty': CommandDifficulty(self.server),
            'players': CommandPlayers(self.server, admin_only=False),
            'game': CommandGame(self.server, admin_only=False),
            'map': CommandGameMap(self.server, admin_only=False),
            'help': CommandHelp(self.server, admin_only=False),
            'info': CommandInfo(self.server, admin_only=False),
            'kills': CommandKills(self.server, admin_only=False),
            'dosh': CommandDosh(self.server, admin_only=False),
            'time': CommandTime(self.server, admin_only=False),
            'top_kills': CommandTopKills(self.server, admin_only=False),
            'top_dosh': CommandTopDosh(self.server, admin_only=False),
            'me': CommandMe(self.server, admin_only=False),
            'stats': CommandStats(self.server, admin_only=False),
            'server_kills': CommandServerKills(self.server, admin_only=False),
            'server_dosh': CommandServerDosh(self.server, admin_only=False),
        }

        return command_map
>>>>>>> master
