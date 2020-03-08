freeze('$(PORT_DIR)/modules')

# entur-micropython libs
freeze('$(PORT_DIR)/../../../../src', 'clock.py')
freeze('$(PORT_DIR)/../../../../src', 'config.py')
# freeze('$(PORT_DIR)/../../../../src', 'configserver.py')
freeze('$(PORT_DIR)/../../../../src', 'display.py')
freeze('$(PORT_DIR)/../../../../src', 'entur.py')
freeze('$(PORT_DIR)/../../../../src', 'log.py')
freeze('$(PORT_DIR)/../../../../src', 'max7219.py')
freeze('$(PORT_DIR)/../../../../src', 'ntptime.py')
freeze('$(PORT_DIR)/../../../../src', 'util.py')
freeze('$(PORT_DIR)/../../../../src', 'wifi.py')

# file utilities
freeze('$(MPY_LIB_DIR)/upysh', 'upysh.py')

# uasyncio
freeze('$(MPY_LIB_DIR)/uasyncio', 'uasyncio/__init__.py')
freeze('$(MPY_LIB_DIR)/uasyncio.core', 'uasyncio/core.py')

# requests
freeze('$(MPY_LIB_DIR)/urequests', 'urequests.py')
freeze('$(MPY_LIB_DIR)/urllib.urequest', 'urllib/urequest.py')
