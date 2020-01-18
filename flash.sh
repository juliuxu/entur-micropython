#!/bin/bash

# Sync code
rsync -rtP . julian@192.168.1.85:code/entur-micropython/ ;and

# Compile firmware
ssh julian@192.168.1.85 "make -C code/entur-micropython/" ;and

# Fetch
scp julian@192.168.1.85:code/entur-micropython/build/micropython/ports/esp8266/build-GENERIC/firmware-combined.bin .

# Flash
esptool.py --chip esp8266 --port /dev/cu.wchusbserial14640 --baud 460800 write_flash --flash_size=detect 0 firmware-combined.bin
