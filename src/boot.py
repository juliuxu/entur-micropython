import gc
import os
import upip
import machine
import wifi
import log
import clock
import config

gc.collect()


# TODO: Move to own file
def install_dependencies():
    log.info("install_dependencies")
    DEPENDENCIES = []
    for (packageName, importName) in DEPENDENCIES:
        try:
            os.stat('/lib/' + importName)
        except OSError:
            log.info("installing %s" % packageName)
            upip.install(packageName)


log.setup()
config.setup()
wifi.setup()

# Ensure wifi
for _ in range(50):
    if wifi.isconnected():
        break
    log.blink(log.WAITING_LED)
    machine.sleep(200)
else:
    log.error("could not connect to wifi")
    log.set_error()

# Set time
clock.setup()
log.success("sat the time")

# Install dependencies
if wifi.isconnected():
    try:
        install_dependencies()
        log.success("all dependencies are installed")
    except Exception:
        log.error("failed installing dependencies")
        log.set_error()
else:
    log.set_waiting()
