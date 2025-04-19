import time
import board
import analogio
import neopixel

# === FSR Setup ===
fsr = analogio.AnalogIn(board.A0)  # A0 = analog input for FSR

# === NeoPixel Setup ===
NUM_PIXELS = 24
pixels = neopixel.NeoPixel(board.A3, NUM_PIXELS, brightness=0.3, auto_write=True, pixel_order=neopixel.GRB)

# Test light-up
pixels.fill((0, 255, 0))  # Green

while True:
    value = fsr.value
    voltage = value * 3.3 / 65535
    print(f"FSR: {value}, Voltage: {voltage:.2f}V")
    time.sleep(0.1)
# Write your code here :-)
