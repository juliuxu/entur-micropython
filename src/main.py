import sys
import log
import clock
import utime as time
import display
import machine
import entur
import config


def get_current_time_text():
    (_, _, _, hour, minute, _, _, _) = clock.localtime()
    s = str(minute)
    if minute < 10:
        s = "0" + s
    s = str(hour) + s
    if hour < 10:
        s = "0" + s
    return s


def seconds_to_text(seconds):
    if seconds < 46:
        return "now"

    if seconds > 584:
        # TODO: Show absolute time
        pass

    return str(int(((seconds - 45) / 60) + 1)) + "m"


def action_departure():
    # Fetch departures
    departures = entur.get_departures()

    # Get first next one
    now_seconds = clock.gettime()
    filtered_departures = filter(lambda x: (
        time.mktime(x + (0, 0)) -
        now_seconds > config.get()["departure_threshold"]
    ), departures)
    next_departure = next(filtered_departures)

    # Display the time till departure
    diff = time.mktime(next_departure + (0, 0)) - clock.gettime()
    next_departure_text = seconds_to_text(diff)
    log.debug("next: %s" % next_departure_text)
    display.text(next_departure_text)


def action_time():
    current_time_text = get_current_time_text()
    log.debug("time: %s" % current_time_text)
    display.text(current_time_text)


STATES = {
    "time": {
        "f": action_time,
        "next": "departure"
    },
    "departure": {
        "f": action_departure,
        "next": "time"
    }
}


def main():
    action_time()
    state = "time"
    while True:
        state = STATES[state]["next"]
        log.info("state -> %s" % state)
        try:
            STATES[state]["f"]()
        except Exception as e:
            log.error("failed on state(%s) " % state)
            log.set_error()
            sys.print_exception(e)  # pylint: disable=no-member
            machine.sleep(10000)
        machine.sleep(config.get()["toggle_delay"])


main()
