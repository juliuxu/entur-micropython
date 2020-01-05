import gc
import sys
import configserver
import uasyncio as asyncio
import log
import clock
import utime as time
import display
import entur
import config
import wifi
import machine


def get_current_time_text():
    (_, _, _, hour, minute, _, _, _) = clock.localtime()
    s = str(minute)
    if minute < 10:
        s = "0" + s
    s = str(hour) + s
    if hour < 10:
        s = "0" + s
    return s


def seconds_to_text_min(seconds):
    if seconds < 60:
        return "now"
    elif seconds > 60*15:
        pass
    return "%dm" % seconds


def seconds_to_text_45(seconds):
    if seconds < 46:
        return "now"

    if seconds > 584:
        # TODO: Show absolute time
        pass

    return str(int(((seconds - 45) / 60) + 1)) + "m"


async def action_departure():
    # Fetch departures
    log.debug("free memory")
    log.debug(gc.mem_free())
    departures = entur.get_departures()

    # Get first next one
    now_seconds = clock.gettime()
    filtered_departures = filter(lambda x: (
        time.mktime(x + (0, 0)) -
        now_seconds > config.get("departure_threshold")
    ), departures)
    next_departure = next(filtered_departures)

    # Display the time till departure
    diff = time.mktime(next_departure + (0, 0)) - clock.gettime()
    next_departure_text = seconds_to_text_45(diff)
    log.debug("next: %s" % next_departure_text)
    display.text(next_departure_text)

    return "time"


async def action_time():
    current_time_text = get_current_time_text()
    log.debug("time: %s" % current_time_text)
    display.text(current_time_text)

    return "departure"


async def action_checkready():
    if not wifi.isconnected():
        status = wifi.get_wifi_status()
        await display.scroll_text("wifi(%s)" % status)
        await display.scroll_text("ap(%s)" % wifi.get_ap_ip())
        return "checkready"
    if config.get("quay_id") == "":
        await display.scroll_text("quay not configured")
        return "checkready"

    return "departure"


async def main():
    STATES = {
        "checkready": action_checkready,
        "time": action_time,
        "departure": action_departure,
    }
    state = "checkready"
    while True:
        log.info("state -> %s" % state)
        try:
            state = await STATES[state]()
        except Exception as e:
            log.error("failed on state(%s) " % state)
            log.set_error()
            sys.print_exception(e)  # pylint: disable=no-member
            gc.collect()
            await asyncio.sleep_ms(10000)  # pylint: disable=no-member
        # pylint: disable=no-member
        gc.collect()
        await asyncio.sleep_ms(config.get("toggle_delay"))
        machine.sleep(1000)


def async_main():
    loop = asyncio.get_event_loop()  # pylint: disable=no-member

    loop.call_soon(asyncio.start_server(  # pylint: disable=no-member
        configserver.handle_request, "0.0.0.0", 80))

    loop.call_soon(main())

    loop.run_forever()
    loop.close()


def rdep():
    loop = asyncio.get_event_loop()  # pylint: disable=no-member
    loop.run_until_complete(action_departure())


if __name__ == "__main__":
    pass
    # main()
    # async_main()
