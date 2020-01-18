
import urequests
import log
import utime as time
from machine import RTC
import ntptime
from util import cache


@cache(3600 * 1000)
def get_offset_from_api():
    log.info("fetching utc_offset from worldtimeapi.org")

    response = urequests.get(
        "http://worldtimeapi.org/api/ip")

    try:
        result = response.json()
        if response.status_code != 200:
            raise Exception
    except Exception as e:
        log.error("failed fetching utc_offset")
        raise e
    finally:
        response.close()

    utc_offset_str = str(result["utc_offset"])
    sign = int(utc_offset_str[0:1] + "1")
    hour = int(utc_offset_str[1:3])
    minute = int(utc_offset_str[4:7])

    return (sign * hour, sign * minute)


@cache(60 * 1000)
def settime():
    (hour_offset, minute_offset) = get_offset_from_api()
    log.info("fetching time from ntp")
    ntptime.settime()

    # add offset
    rtc = RTC()
    (year, month, day, _, hour, minute, second, subsecond) = rtc.datetime()
    rtc.datetime((year, month, day, 0, hour + hour_offset,
                  minute + minute_offset, second, subsecond))


def localtime():
    settime()
    return time.localtime()


def gettime():
    settime()
    return time.time()


def setup():
    settime()
