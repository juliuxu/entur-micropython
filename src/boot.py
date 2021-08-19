import gc
import machine
import wifi
import log
import clock
import display
import uasyncio as asyncio


def boot():
    gc.collect()
    log.setup()
    # config.setup()

    # Setup display
    display.setup()
    log.success("display setup")

    display.text("wifi")
    wifi.setup()

    log.info("trying to connect to wifi")
    for _ in range(25):
        if wifi.isconnected():
            log.success("connected to wifi {}".format(wifi.get_wifi_ip()))
            break
        machine.sleep(200)
    else:
        log.error("could not connect to wifi")
        return

    # pylint: disable=no-member
    #asyncio.get_event_loop().run_until_complete(
    #    display.scroll_text("{}".format(wifi.get_wifi_ip())))
    machine.sleep(500)

    # Set time
    display.text("time")
    clock.setup()
    log.success("time is synced")

    display.text("done")


boot()
