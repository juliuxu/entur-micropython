# pylint: disable=global-statement
import network
import config

_sta_if = None


def setup():
    global _sta_if
    _sta_if = network.WLAN(network.STA_IF)
    _sta_if.active(True)
    _sta_if.connect(config.get()["wifi_essid"], config.get()["wifi_password"])


def isconnected():
    global _sta_if
    return _sta_if.isconnected()
