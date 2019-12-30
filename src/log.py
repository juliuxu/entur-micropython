import sys
import machine

_stream = sys.stderr

SUCCESS_LED = machine.Pin(15, machine.Pin.OUT)
ERROR_LED = machine.Pin(13, machine.Pin.OUT)
WAITING_LED = machine.Pin(12, machine.Pin.OUT)


def zero_leds():
    for led in [SUCCESS_LED, ERROR_LED, WAITING_LED]:
        led.off()


def blink(led, delay=100):
    led.on()
    machine.sleep(delay)
    led.off()
    machine.sleep(delay)


def blink_times(led, delay, times):
    for _ in range(times):
        blink(led, delay)


def set_success():
    zero_leds()
    SUCCESS_LED.on()


def set_error():
    zero_leds()
    ERROR_LED.on()


def set_waiting():
    zero_leds()
    WAITING_LED.on()


def _log(level, msg, *args):
    zero_leds()

    _stream.write("[%s]: " % (level))
    if not args:
        print(msg, file=_stream)
    else:
        print(msg % args, file=_stream)


def info(msg, *args):
    _log("INFO", msg, *args)


def debug(msg, *args):
    _log("DEBUG", msg, *args)


def error(msg, *args):
    _log("ERROR", msg, *args)


def success(msg, *args):
    _log("SUCCESS", msg, *args)
    blink(SUCCESS_LED)


def setup():
    zero_leds()
