
import urequests
import log
from machine import RTC
import ntptime
from util import cache


rtc = RTC()


@cache(3600 * 1000)
def get_offset_from_api():
    log.debug("fetching utc_offset from worldtimeapi.org")

    response = urequests.get(
        "http://worldtimeapi.org/api/ip")
    if response.status_code != 200:
        log.error("failed fetching utc_offset")
        log.set_error()
        raise RuntimeError("failed fetching utc_offset")

    parsed = response.json()
    log.debug(parsed)

    utc_offset_str = str(parsed["utc_offset"])
    sign = int(utc_offset_str[0:1] + "1")
    hour = int(utc_offset_str[1:3])
    minute = int(utc_offset_str[4:7])

    return (sign * hour, sign * minute)


@cache(60 * 1000)
def settime():
    (hour_offset, minute_offset) = get_offset_from_api()
    ntptime.settime()

    # add offset
    (year, month, day, _, hour, minute, second, subsecond) = rtc.datetime()
    rtc.datetime((year, month, day, 0, hour + hour_offset,
                  minute + minute_offset, second, subsecond))


def setup():
    settime()
