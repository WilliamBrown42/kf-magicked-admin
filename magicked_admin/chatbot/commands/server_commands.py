from chatbot.commands.command import Command


from os import path

class CommandSay(Command):
<<<<<<< HEAD
    def __init__(self, operator_list, admin=True):
        Command.__init__(self, operator_list, admin)
=======
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "No message was specified."

        message = " ".join(args[1:])
        # Unescape escape characters in say command
        message = bytes(message.encode("iso-8859-1", "ignore"))\
            .decode('unicode_escape')
        return message

<<<<<<< HEAD

class CommandRestart(Command):
    def __init__(self, operator_list, web_admin, admin=True):
        self.web_admin = web_admin

        Command.__init__(self, operator_list, admin)
=======
class CommandEnforceLevels(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        self.server.enforce_levels()


class CommandRun(Command):
    def __init__(self, server, chatbot, admin_only=True):
        Command.__init__(self, server, admin_only)

        self.chatbot = chatbot

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "No file was specified."

        if not path.exists(args[1]):
            return "File not found"

        self.chatbot.execute_script(args[1])

        return


class CommandRestart(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
<<<<<<< HEAD
        
        self.web_admin.restart_map()
        return "Restarting map."


class CommandTogglePassword(Command):
    def __init__(self, operator_list, web_admin, admin=True):
        self.web_admin = web_admin

        Command.__init__(self, operator_list, admin)
=======

        self.server.restart_map()
        return "Restarting map."


class CommandLoadMap(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
<<<<<<< HEAD
        
        new_state = self.web_admin.toggle_game_password()
        if new_state:
            return "Game password enabled"
        else:
            return "Game password disabled"


class CommandSilent(Command):
    def __init__(self, operator_list, chatbot, admin=True):
        self.chatbot = chatbot

        Command.__init__(self, operator_list, admin)
=======

        if len(args) < 2:
            return "Missing argument (map name)"

        self.server.change_map(args[1])
        return "Changing map."


class commandDisablePassword(Command):
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        new_state = self.server.disable_password()

        if new_state:
            return "Game password disabled"
        else:
            return "Game password not disabled, please try again"


class CommandEnablePassword(Command):
    """
    """
    def __init__(self, server, admin_only=True):
        Command.__init__(self, server, admin_only)

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        # Args are for starting the timer for inactivity.
        if len(args) > 1 and args[1] == '-t':
            new_state = self.server.enable_password(True)
        else:
            new_state = self.server.enable_password(False)

        if new_state:
            return "Game password enabled"
        else:
            return "Game password not enabled, please try again."


class CommandSilent(Command):
    def __init__(self, server, chatbot, admin_only=True):
        self.chatbot = chatbot
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message

        if self.chatbot.silent:
            self.chatbot.silent = False
            return None
        else:
            self.chatbot.command_handler("server", "say Silent mode enabled.",
                                         admin=True)
            self.chatbot.silent = True


class CommandLength(Command):
<<<<<<< HEAD
    def __init__(self, operator_list, web_admin, admin=True):
        self.web_admin = web_admin

        Command.__init__(self, operator_list, admin)
=======
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
            return "Length not recognised. Options are short, medium, or long."
<<<<<<< HEAD
        
        if args[1] == "short":
            length = self.web_admin.LEN_SHORT
        elif args[1] == "medium":
            length = self.web_admin.LEN_NORM
        elif args[1] == "long":
            length = self.web_admin.LEN_LONG
        else:
            return "Length not recognised. Options are short, medium, or long."
        
        self.web_admin.set_length(length)
=======

        if args[1] in ["short", "0"]:
            length = server.LEN_SHORT
        elif args[1] in ["medium", "med", "normal", "1"]:
            length = server.LEN_NORM
        elif args[1] in ["long", "2"]:
            length = server.LEN_LONG
        else:
            return "Length not recognised. Options are short, medium, or long."

        self.server.set_length(length)
>>>>>>> master
        return "Length change will take effect next game."


class CommandDifficulty(Command):
<<<<<<< HEAD
    def __init__(self, operator_list, web_admin, admin=True):
        self.web_admin = web_admin

        Command.__init__(self, operator_list, admin)
=======
    def __init__(self, server, admin_only = True):
        Command.__init__(self, server, admin_only)
>>>>>>> master

    def execute(self, username, args, admin):
        if not self.authorise(admin):
            return self.not_auth_message
        if len(args) < 2:
<<<<<<< HEAD
            return "Difficulty not recognised. Options are normal, hard, suicidal, or hell."
        
        if args[1] == "normal":
            difficulty = self.web_admin.DIFF_NORM
        elif args[1] == "hard":
            difficulty = self.web_admin.DIFF_HARD
        elif args[1] == "suicidal":
            difficulty = self.web_admin.DIFF_SUI
        elif args[1] == "hell":
            difficulty = self.web_admin.DIFF_HOE
=======
            return "Difficulty not recognised. " + \
                   "Options are normal, hard, suicidal, or hell."

        if args[1] in ["normal", "0"]:
            difficulty = server.DIFF_NORM
        elif args[1] in ["hard", "1"]:
            difficulty = server.DIFF_HARD
        elif args[1] in ["suicidal", "sui", "2"]:
            difficulty = server.DIFF_SUI
        elif args[1] in ["hell", "hoe", "hellonearth", "3"]:
            difficulty = server.DIFF_HOE
>>>>>>> master
        else:
            return "Difficulty not recognised. " + \
                   "Options are normal, hard, suicidal, or hell."

        self.server.set_difficulty(difficulty)
        return "Difficulty change will take effect next game."
