import board
import os
import analogio
import neopixel
import time
import alarm
import microcontroller
from fade_controller import Fade_Controller
from press_observer import Press_Duration_Observer


# === SETUP CONSTANTS ===
SLEEP_TIME = os.getenv("SLEEP_TIME")
ALPHA = 0.5 # FSR signal smoothing factor


# === SETUP NEOPIXEL ===
PIXEL_ORDER = getattr(neopixel, os.getenv("PIXEL_ORDER"))
pixels = neopixel.NeoPixel(
    pin = getattr(board, os.getenv("NEOPIXEL_PIN")), 
    n = os.getenv("NUM_PIXELS"), 
    bpp = len(PIXEL_ORDER), 
    brightness = float(os.getenv("BRIGHTNESS")), 
    auto_write = True, 
    pixel_order = PIXEL_ORDER
    )

# === SETUP FSR === 
fsr = analogio.AnalogIn(getattr(board, os.getenv("FSR_PIN")))

# === SETUP FADER AND PRESS OBSERVER ===
COLOR = tuple(int(i.strip()) for i in os.getenv("COLOR")[1:-1].split(','))
fader = Fade_Controller(pixels, COLOR)
press_observer = Press_Duration_Observer(float(os.getenv("PRESS_DURATION_THRESHOLD")), 63000)

# === FADE UP NEOPIXELS === 
while not fader.is_finished():
    fader.fade_up()
    time.sleep(.01)
    
#  === WAIT FOR SENSOR TO BE PRESSED ===
filtered_value = fsr.value
while not press_observer.duration_passed():
    filtered_value = ALPHA * fsr.value + (1-ALPHA) * filtered_value
    press_observer.update(filtered_value)
    if press_observer.press_started:
        fader.fade_down(0.2)
    else:
        fader.fade_up()
    time.sleep(.01)

# === FADE DOWN NEOPIXELS ===
while not fader.is_finished():
    fader.fade_down()
    time.sleep(0.01)

# === ENTER SLEEP ===
print(f"Going to sleep for {SLEEP_TIME} seconds...")
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + SLEEP_TIME)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)


# === Hard reset on wake-up ===
# This line will only execute if somehow deep sleep fails
microcontroller.reset()
# Write your code here :-)