import gc
import machine
import wifi
import log
import clock
import config
import display


def boot():
    gc.collect()
    log.setup()
    config.setup()

    # Setup display
    display.setup()
    log.success("display setup")

    display.text("wifi")
    wifi.setup()

    # Ensure wifi
    for _ in range(50):
        if wifi.isconnected():
            log.success("connected to wifi")
            break
        log.blink(log.WAITING_LED)
        machine.sleep(200)
    else:
        log.error("could not connect to wifi")
        log.set_error()
        return

    # Set time
    display.text("time")
    clock.setup()
    log.success("sat the time")

    display.text("done")


boot()
