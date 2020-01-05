# pylint: disable=global-statement
import ujson as json
import log


CONFIG_FILE_NAME = "/config.json"

_config = {}

CONFIG_SCHEMA = {
    "wifi_essid": str,
    "wifi_password": str,
    "toggle_delay": int,
    "quay_id": str,
    "departure_threshold": int
}


def ensure_keys(d):
    for (key, value) in d.items():
        if key not in CONFIG_SCHEMA:
            return False
        if not isinstance(value, CONFIG_SCHEMA[key]):
            return False
    return True


def load():
    try:
        with open(CONFIG_FILE_NAME) as f:
            return json.loads(f.read())
    except OSError:
        log.error("could not open config file")
        log.set_error()


def save():
    try:
        with open(CONFIG_FILE_NAME, 'wb') as f:
            json.dump(_config, f)
        return True
    except OSError:
        log.error("could not save config file")
        log.set_error()
        return False


def get(key):
    return _config[key]


def set_config(new_config):
    global _config
    if not ensure_keys(new_config):
        return False
    _config = new_config
    save()
    return True


def setup():
    global _config
    _config = load()
