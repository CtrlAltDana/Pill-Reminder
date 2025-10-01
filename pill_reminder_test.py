import time
import board
import analogio
import neopixel
from ulab import numpy as np

# === FSR Setup ===
fsr = analogio.AnalogIn(board.A0)  # A0 = analog input for FSR

# === NeoPixel Setup ===
NUM_PIXELS = 24

# For RGBW
pixels = neopixel.NeoPixel(
    board.A3, NUM_PIXELS, brightness=0.05, auto_write=True, pixel_order=neopixel.GRBW
)
# For RGB
# pixels = neopixel.NeoPixel(
#     board.A3, NUM_PIXELS, brightness=0.05, auto_write=True, pixel_order=neopixel.GRB
# )

# Test light-up
pixels.fill((0, 255, 0, 50))  # For RGBW
# pixels.fill((0, 255, 0)) # For RGB
values = []
while True:
    value = fsr.value
    voltage = value * 3.3 / 65535
    values.append(value)
    if len(values) / 4 == 1:
        mean = np.sum(values) / len(values)
        print((mean,))
        values = []
    time.sleep(.1)
