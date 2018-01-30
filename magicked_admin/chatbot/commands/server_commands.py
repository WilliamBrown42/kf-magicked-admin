from chatbot.commands.command import Command
import server.server as server


class CommandSay(Command):
    def __init__(self, operator_list, admin=True):
        Command.__init__(self, operator_list, admin)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "No message was specified."
                
        message = " ".join(args[1:])
        # Unescape escape characters in say command
        message = bytes(message.encode("iso-8859-1","ignore")).decode('unicode_escape')
        return message


class CommandRestart(Command):
    def __init__(self, operator_list, web_admin, admin=True):
        self.web_admin = web_admin

        Command.__init__(self, operator_list, admin)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        self.web_admin.restart_map()
        return "Restarting map."


class CommandTogglePassword(Command):
    def __init__(self, operator_list, web_admin, admin=True):
        self.web_admin = web_admin

        Command.__init__(self, operator_list, admin)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        new_state = self.web_admin.toggle_game_password()
        if new_state:
            return "Game password enabled"
        else:
            return "Game password disabled"


class CommandSilent(Command):
    def __init__(self, operator_list, chatbot, admin=True):
        self.chatbot = chatbot

        Command.__init__(self, operator_list, admin)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        
        if self.chatbot.silent:
            self.chatbot.silent = False 
            return "Silent mode disabled."
        else:
            self.chatbot.command_handler("server", "say Silent mode enabled.", admin=True)
            self.chatbot.silent = True


class CommandLength(Command):
    def __init__(self, operator_list, web_admin, admin=True):
        self.web_admin = web_admin

        Command.__init__(self, operator_list, admin)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "Length not recognised. Options are short, medium, or long."
        
        if args[1] == "short":
            length = self.web_admin.LEN_SHORT
        elif args[1] == "medium":
            length = self.web_admin.LEN_NORM
        elif args[1] == "long":
            length = self.web_admin.LEN_LONG
        else:
            return "Length not recognised. Options are short, medium, or long."
        
        self.web_admin.set_length(length)
        return "Length change will take effect next game."


class CommandDifficulty(Command):
    def __init__(self, operator_list, web_admin, admin=True):
        self.web_admin = web_admin

        Command.__init__(self, operator_list, admin)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "Difficulty not recognised. Options are normal, hard, suicidal, or hell."
        
        if args[1] == "normal":
            difficulty = self.web_admin.DIFF_NORM
        elif args[1] == "hard":
            difficulty = self.web_admin.DIFF_HARD
        elif args[1] == "suicidal":
            difficulty = self.web_admin.DIFF_SUI
        elif args[1] == "hell":
            difficulty = self.web_admin.DIFF_HOE
        else:
            return "Difficulty not recognised. Options are normal, hard, suicidal, or hell."
        
        self.server.set_difficulty(difficulty)
        return "Difficulty change will take effect next game."
