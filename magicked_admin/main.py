import configparser
import os
import signal
import sys

from server.server import Server

DEBUG = True

if not os.path.exists("./magicked_admin.conf"):
    sys.exit("Configuration file not found.")
config = configparser.ConfigParser()
config.read("./magicked_admin.conf")


class MagickedAdministrator:
    
    def __init__(self):
        self.servers = []
        signal.signal(signal.SIGINT, self.terminate)

    def run(self):
        for server_name in config.sections():
            config[server_name]["name"] = server_name
            server = Server(config[server_name])

            self.servers.append(server)
            server.start()

        print("INFO: All Servers started\n")
            
    def terminate(self, signal, frame):
        print("\nINFO: Terminating...")
        for server in self.servers:
            server.terminate()


if __name__ == "__main__":
    application = MagickedAdministrator()
    application.run()

    sys.exit(0)
