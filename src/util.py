import utime


def parse_iso8601(s):
    year = int(s[0:4])
    month = int(s[5:7])
    day = int(s[8:10])
    hour = int(s[11:13])
    minute = int(s[14:16])
    second = int(s[17:19])
    return (year, month, day, hour, minute, second)


def cache(period_ms):
    def inner(f):
        cache_dict = {
            "ticks_ms": None,
            "result": None
        }

        def inner2(*args):
            if cache_dict["ticks_ms"] is None or utime.ticks_diff(utime.ticks_ms(), cache_dict["ticks_ms"]) > period_ms:
                cache_dict["result"] = f(*args)
                cache_dict["ticks_ms"] = utime.ticks_ms()
            return cache_dict["result"]
        return inner2
    return inner
