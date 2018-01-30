from chatbot.commands.player_commands import *
from chatbot.commands.info_commands import *
from chatbot.commands.server_commands import *
#from chatbot.commands.event_commands import *


def build_command_map(chatbot, admin_commands):
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
        'say': CommandSay(server,
                          admin='say' in admin_commands),
        'restart': CommandRestart(server,
                                  admin='restart' in admin_commands),
        'toggle_pass': CommandTogglePassword(server,
                                             admin=
                                             'toggle_pass' in admin_commands),
        'silent': CommandSilent(server,
                                admin='silent' in admin_commands),
        'length': CommandLength(server,
                                admin='length' in admin_commands),
        'difficulty': CommandDifficulty(server,
                                        admin='difficulty' in admin_commands),
        'players': CommandPlayers(server,
                                  admin='players' in admin_commands),
        'game': CommandGame(server,
                            admin='game' in admin_commands),
        'help': CommandHelp(server,
                            admin='help' in admin_commands),
        'info': CommandInfo(server,
                            admin='info' in admin_commands),
        'kills': CommandKills(server,
                              admin='kills' in admin_commands),
        'dosh': CommandDosh(server,
                            admin='dosh' in admin_commands),
        'top_kills': CommandTopKills(server,
                                     admin='top_kills' in admin_commands),
        'top_dosh': CommandTopDosh(server,
                                   admin='top_dosh' in admin_commands),
        'me': CommandMe(server,
                        admin='me' in admin_commands),
        'stats': CommandStats(server,
                              admin='stats' in admin_commands)
    }

    return command_map

'''
class CommandMap:
    
    def __init__(self, server, chatbot, admin_commands):
        self.admin_commands = admin_commands
        self.server = server
        self.chatbot = chatbot
        self.command_map = self.generate_map()

    def generate_map(self):
        wave_event_manager = CommandOnWaveManager(self.server, self.chatbot)
        trader_event_manager = CommandOnTraderManager(self.server, self.chatbot)
        time_event_manager = CommandOnTimeManager(self.server, self.chatbot)
        
        command_map = {
            'stop_wc': wave_event_manager,
            'start_wc': wave_event_manager,
            'new_wave': wave_event_manager,
            'start_tc': time_event_manager,
            'stop_tc': time_event_manager,
            'start_trc': trader_event_manager,
            'stop_trc': trader_event_manager,
            't_close': trader_event_manager,
            't_open': trader_event_manager,
            'say': CommandSay(self.server,
                              admin='me' in self.admin_commands),
            'restart': CommandRestart(self.server,
                                      admin='me' in self.admin_commands),
            'toggle_pass': CommandTogglePassword(self.server,
                                                 admin='me' in self.admin_commands),
            'silent': CommandSilent(self.server,
                                    admin='me' in self.admin_commands),
            'length': CommandLength(self.server,
                                    admin='me' in self.admin_commands),
            'difficulty': CommandDifficulty(self.server,
                                            admin='me' in self.admin_commands),
            'players': CommandPlayers(self.server,
                                      admin='me' in self.admin_commands),
            'game': CommandGame(self.server,
                                admin='me' in self.admin_commands),
            'help': CommandHelp(self.server,
                                admin='me' in self.admin_commands),
            'info': CommandInfo(self.server,
                                admin='me' in self.admin_commands),
            'kills': CommandKills(self.server,
                                  admin='me' in self.admin_commands),
            'dosh': CommandDosh(self.server,
                                admin='me' in self.admin_commands),
            'top_kills': CommandTopKills(self.server,
                                         admin='me' in self.admin_commands),
            'top_dosh': CommandTopDosh(self.server,
                                       admin='me' in self.admin_commands),
            'me': CommandMe(self.server,
                            admin='me' in self.admin_commands),
            'stats': CommandStats(self.server,
                                  admin='stats' in self.admin_commands)
        }
        
        return command_map
'''
