import micropython as m
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

gc.collect()


def get_current_time_text():
    (_, _, _, hour, minute, _, _, _) = clock.localtime()
    return "{:02d}{:02d}".format(hour, minute)


def seconds_to_text_min(seconds):
    if seconds < 60:
        return "now"
    if seconds > 60*15:
        pass
    return "{}m".format(seconds)


def seconds_to_text_45(seconds):
    if seconds < 46:
        return "now"

    # if seconds > 584:
        # TODO: Show absolute time
        # pass

    return "{}m".format(int(((seconds - 45) / 60) + 1))


async def action_departure():
    # Fetch departure
    departure = entur.get_departures()
    gc.collect()

    # Get first next one
    now_seconds = clock.gettime()
    filtered_departures = filter(lambda x: (
        time.mktime(x[0] + (0, 0)) -
        now_seconds > config.get("departure_threshold")
    ), departure)
    next_departure = next(filtered_departures)

    # Display the time till departure
    diff = time.mktime(next_departure[0] + (0, 0)) - clock.gettime()
    next_departure_text = seconds_to_text_45(diff)
    if next_departure[1] is True:
        next_departure_text += "!"
    if __debug__:
        log.debug("next: {}".format(next_departure_text))
    display.text(next_departure_text)

    return "time"


async def action_time():
    current_time_text = get_current_time_text()
    if __debug__:
        log.debug("time: {}".format(current_time_text))
    display.text(current_time_text)

    return "departure"


async def action_checkready():
    if not wifi.isconnected():
        status = wifi.get_wifi_status()
        await display.scroll_text("wifi({})".format(status))
        await display.scroll_text("ap({})".format(wifi.get_ap_ip()))
        return "checkready"
    if config.get("quay_id") == "":
        await display.scroll_text("quay not configured")
        return "checkready"

    return "time"


async def main():
    STATES = {
        "checkready": action_checkready,
        "time": action_time,
        "departure": action_departure,
    }
    state = "checkready"
    exCount = 0
    while True:
        gc.collect()
        if __debug__:
            log.debug("state -> {}".format(state))
            log.debug('free: {} allocated: {}'.format(
                gc.mem_free(), gc.mem_alloc()))  # pylint: disable=no-member
            m.mem_info()

        try:
            state = await STATES[state]()
        except Exception as e:
            exCount += 1
            if exCount > 5:
                machine.reset()
            display.text("err")
            log.error("failed on state({}) ".format(state))
            sys.print_exception(e)  # pylint: disable=no-member
            await asyncio.sleep_ms(10000)  # pylint: disable=no-member
        await asyncio.sleep_ms(config.get("toggle_delay"))  # pylint: disable=no-member


def async_main():
    loop = asyncio.get_event_loop()  # pylint: disable=no-member

    loop.call_soon(asyncio.start_server(  # pylint: disable=no-member
        configserver.handle_request, "0.0.0.0", 80))

    loop.call_soon(main())

    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    async_main()
