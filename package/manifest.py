include('manifest.py')

# file utilities
freeze('$(MPY_LIB_DIR)/upysh', 'upysh.py')

# uasyncio
freeze('$(MPY_LIB_DIR)/uasyncio', 'uasyncio/__init__.py')
freeze('$(MPY_LIB_DIR)/uasyncio.core', 'uasyncio/core.py')

# requests
freeze('$(MPY_LIB_DIR)/urequests', 'urequests.py')
freeze('$(MPY_LIB_DIR)/urllib.urequest', 'urllib/urequest.py')
