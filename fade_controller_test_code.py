import board
import neopixel
from fade_controller import Fade_Controller
import time

NEOPIXEL_PIN = board.A3
pixels = neopixel.NeoPixel(
    NEOPIXEL_PIN,
    24,
    brightness=.4,
    auto_write=True,
    pixel_order=neopixel.GRBW  # RGBW-only
)
PIXEL_COLOR = (255, 0, 255, 0)

pixels.fill((0, 0, 0, 0))

fader = Fade_Controller(pixels, PIXEL_COLOR)

time.sleep(2)

while True:
    fader.breath()
