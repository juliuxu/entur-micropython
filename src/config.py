# pylint: disable=global-statement
import ujson as json
import log


CONFIG_FILE_NAME = "config.json"

_config = {}


def load():
    try:
        with open(CONFIG_FILE_NAME) as f:
            return json.loads(f.read())
    except OSError:
        log.error("could not open config file")
        log.set_error()


def get():
    return _config


def setup():
    global _config
    _config = load()
