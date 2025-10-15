import time
import board
import analogio
import neopixel
from press_observer import Press_Duration_Observer
from ulab import numpy as np
from fade_controller import Fade_Controller

# === FSR Setup ===
fsr = analogio.AnalogIn(board.A2)  # A0 = analog input for FSR

# === NeoPixel Setup ===
NUM_PIXELS = 24

# For RGBW
#pixels = neopixel.NeoPixel(
#    board.A3, NUM_PIXELS, brightness=0.05, auto_write=True, pixel_order=neopixel.GRW
#)
# For RGB
pixels = neopixel.NeoPixel(board.D3, NUM_PIXELS, brightness=0.5, auto_write=True, pixel_order=neopixel.GRB)

print(getattr(board, "D3"))

# Test light-up
PIXEL_COLOR = (255, 0, 255)
#pixels.fill() # For RGB
values = []
filtered_value = fsr.value
ALPHA = .5
fader = Fade_Controller(pixels, PIXEL_COLOR)
press_observer = Press_Duration_Observer(5, 64000)
#pressure_trigger.start()


# Fade up LEDs
while not fader.is_finished():
    fader.fade_up()
    time.sleep(.01)


# Wait for sensor to pressed
while not press_observer.duration_passed():
    value = fsr.value
    filtered_value = ALPHA * value + (1-ALPHA) * filtered_value
    press_observer.update(filtered_value)
    if press_observer.press_started:
        fader.fade_down(0.2)
    else:
        fader.fade_up()
    #print((filtered_value,))
    time.sleep(.01)


# Fade down LEDs
while not fader.is_finished():
    fader.fade_down()
    time.sleep(0.01)
