# pylint: disable=global-statement
import network
import config
from ubinascii import hexlify

AP_ESSID_PREFIX = "MicroEntur"
AP_PASSWORD = "microentur"


def setup_ap_mode():
    wifi_interface = network.WLAN(network.AP_IF)
    wifi_interface.active(True)
    essid = "{}-{}".format(AP_ESSID_PREFIX,
                           hexlify(wifi_interface.config("mac")[-3:]).decode())
    wifi_interface.config(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK,
                          password=AP_PASSWORD)


def get_ap_ip():
    wifi_interface = network.WLAN(network.AP_IF)
    (ip, _, _, _) = wifi_interface.ifconfig()
    return ip


def get_wifi_status():
    STATUS_CODES = [
        "IDLE",
        "CONNECTING",
        "WRONG_PASSWORD",
        "NO_AP_FOUND",
        "CONNECT_FAIL",
        "GOT_IP"
    ]
    wifi_interface = network.WLAN(network.STA_IF)
    status_code = wifi_interface.status()
    return STATUS_CODES[status_code] if status_code < 6 else "UNKNOWN"


def get_wifi_ip():
    wifi_interface = network.WLAN(network.STA_IF)
    (ip, _, _, _) = wifi_interface.ifconfig()
    return ip


def setup_wifi():
    wifi_interface = network.WLAN(network.STA_IF)
    if config.get("wifi_essid") != "":
        wifi_interface.active(True)
        wifi_interface.connect(config.get("wifi_essid"),
                               config.get("wifi_password"))


def access_point_tuple_to_dict(t):
    AUTHMODES = ["OPEN",
                 "WEP",
                 "WPA-PSK",
                 "WPA2-PSK",
                 "WPA/WPA2-PSK"]

    (ssid, bssid, channel, RSSI, authmode, hidden) = t
    return {
        "ssid": ssid,
        "bssid": hexlify(bssid),
        "channel": channel,
        "RSSI": RSSI,
        "authmode": AUTHMODES[authmode],
        "hidden": True if hidden is 0 else False,
    }


def get_access_points():
    wifi_interface = network.WLAN(network.STA_IF)
    access_points = wifi_interface.scan()
    filtered_access_points = filter(
        lambda x: not x[0].startswith(AP_ESSID_PREFIX), access_points)
    mapped_access_points = map(
        access_point_tuple_to_dict, filtered_access_points)

    return list(mapped_access_points)


def setup():
    setup_ap_mode()
    setup_wifi()


def isconnected():
    wifi_interface = network.WLAN(network.STA_IF)
    return wifi_interface.isconnected()
