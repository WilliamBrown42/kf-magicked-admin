import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_config(config):
    if len(config.sections()) < 1:
        logger.error("config (magicked_admin.conf) contains no servers")
        return False

    for server_name in config.sections():
        if not __check_server_keyset(config, server_name):
            return False

    return True


def __check_server_keyset(config, server_name):
    expected_keys = {
        "address",
        "username",
        "password",
        "game_password",
        "motd_scoreboard",
        "scoreboard_type",
        "operators",
        "operator_commands",
        "help_text"
    }
    actual_keys = set(i[0] for i in list(config.items(server_name)))

    if not expected_keys.issubset(actual_keys):
        logger.error("Server '{}' is missing key(s) {}".format(
            server_name, expected_keys - actual_keys
        ))
        return False

    return True
