import sys


def _log(level, msg):
    _stream = sys.stderr
    _stream.write("[{}]: \t".format(level))
    print(msg, file=_stream)


def info(msg):
    _log("INFO", msg)


def debug(msg):
    _log("DEBUG", msg)


def error(msg):
    _log("ERROR", msg)


def success(msg):
    _log("SUCCESS", msg)


def setup():
    pass
