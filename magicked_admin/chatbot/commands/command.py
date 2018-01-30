

class Command:
    
    def __init__(self, operator_list, admin=True):
        self.admin = admin
        self.operator_list = operator_list
        self.not_auth_message = "You're not authorised to use that command."

    def authorise(self, admin, steam_id=None):
        if self.admin and admin:
            # Return true if player is logged in as admin regardless of op list
            return True

        if self.admin and not admin:
            # Return true if player is an op even if not logged in as admin
            return steam_id in self.operator_list

        # If command doesn't require any permission return true
        return True
            
    def execute(self, username, args, admin):
        raise NotImplementedError("Command.execute() not implemented")

