import utime


def cache(period_ms):
    def inner(f):
        cache_dict = {
            "ticks_ms": None,
            "result": None
        }

        def inner2():
            if cache_dict["result"] is None or utime.ticks_diff(utime.ticks_ms(), cache_dict["ticks_ms"]) > period_ms:
                cache_dict["result"] = f()
                cache_dict["ticks_ms"] = utime.ticks_ms()
            return cache_dict["result"]
        return inner2
    return inner
