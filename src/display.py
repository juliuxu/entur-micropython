# pylint: disable=global-statement
import max7219
from machine import Pin, SPI
import uasyncio

display = None


def text(msg):
    display.fill(0)
    display.text(msg, 0, 0, 1)
    display.show()


async def scroll_text(msg, delay=25):
    d = display
    for i in range((len(msg) + 4) * 8):
        d.fill(0)
        d.text(msg, 8*4 - i, 0, 1)
        d.show()
        await uasyncio.sleep_ms(delay)  # pylint: disable=no-member


def setup():
    global display
    spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
    display = max7219.Matrix8x8(spi, Pin(15), 4)
    display.brightness(0)
    display.fill(0)
