# Entur Client in Micropython for ESP8266

## QUAYS

> A quay is like a platform, which line you are going

- NSR:Quay:12286 Karlsrud mot Sentrum
- NSR:Quay:10851 Manglerud mot Sentrum

## Suggestions

Utropstegn når det er forsinkelse

# Setup instructions

## Get a good cable!

For mac search usb c to usb micro

https://www.kjell.com/no/produkter/data/kabler-og-adaptere/usb/usb-kabler/tilkoblingskabel-usb-c-til-micro-usb-06-m-p69167

## Flash board

https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/

`pip3 install esptool`
`esptool.py --chip esp8266 --port /dev/cu.SLAB_USBtoUART erase_flash`
`esptool.py --chip esp8266 --port /dev/cu.SLAB_USBtoUART --baud 460800 write_flash --flash_size=detect 0 esp8266-20210618-v1.16.bin`

## Connect display

https://mytectutor.com/how-to-control-max7219-led-matrix-with-esp8266-nodemcu-over-wifi/

## Setup pymakr

https://randomnerdtutorials.com/micropython-esp32-esp8266-vs-code-pymakr/
