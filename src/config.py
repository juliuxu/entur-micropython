# pylint: disable=global-statement
import ujson as json
import log


CONFIG_FILE_NAME = "/config.json"

# def ensure_keys(d):
# CONFIG_SCHEMA = {
#     "wifi_essid": str,
#     "wifi_password": str,
#     "toggle_delay": int,
#     "quay_id": str,
#     "departure_threshold": int
# }
# for (key, value) in d.items():
#     if key not in CONFIG_SCHEMA:
#         return False
#     if not isinstance(value, CONFIG_SCHEMA[key]):
#         return False
# return True


def load():
    try:
        with open(CONFIG_FILE_NAME) as f:
            return json.load(f)
    except OSError:
        log.error("could not open config file")


def save(new_config):
    try:
        with open(CONFIG_FILE_NAME, 'wb') as f:
            json.dump(new_config, f)
        return True
    except OSError:
        log.error("could not save config file")
        return False


def get(key):
    return load()[key]


def set_config(new_config):
    # if not ensure_keys(new_config):
    #     return False
    save(new_config)
    return True
