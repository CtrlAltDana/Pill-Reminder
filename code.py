import board
import os
import analogio
import neopixel
import time
import alarm
import microcontroller
from fade_controller import Fade_Controller
from press_observer import Press_Duration_Observer
from smooth import smooth

# === SETUP CONSTANTS ===
SLEEP_TIME = os.getenv("SLEEP_TIME")
ALPHA = 0.5  # FSR signal smoothing factor
FORCE_THRESHOLD = 63000
LOW_FORCE_THRESHOLD = 32000
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

PRESS_DURATION_THRESHOLD = float(os.getenv("PRESS_DURATION_THRESHOLD"))
fader = Fade_Controller(pixels, COLOR, duration=PRESS_DURATION_THRESHOLD*700)
press_observer = Press_Duration_Observer(PRESS_DURATION_THRESHOLD, FORCE_THRESHOLD)

# === FADE UP NEOPIXELS === 
while not fader.is_finished():
    fader.fade_up()
    time.sleep(.01)
    
# === WAIT FOR LOW FSR VALUE ===
filtered_value = fsr.value
while True:
    while filtered_value > LOW_FORCE_THRESHOLD:
        filtered_value = smooth(fsr.value, filtered_value, ALPHA)
        time.sleep(0.01)
    start_time = time.monotonic()
    
    while time.monotonic() - start_time < 1:
        filtered_value = smooth(fsr.value, filtered_value, ALPHA)
        if filtered_value > LOW_FORCE_THRESHOLD:  # if bottle returned too quickly
            break # restart removal check
        time.sleep(.01)
    else:
        print("FSR value remained low for long enough. Proceeding.")
        break
            
    
#  === WAIT FOR SENSOR TO BE PRESSED ===
while not press_observer.duration_passed():
    filtered_value = smooth(fsr.value, filtered_value, ALPHA)
    #print((filtered_value,))
    press_observer.update(filtered_value)
    if press_observer.press_started:
        fader.fade_down()
    else:
        fader.fade_up()
    time.sleep(.01)

# === ENTER SLEEP ===
print(f"Going to sleep for {SLEEP_TIME} seconds...")
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + SLEEP_TIME)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)

# === Hard reset on wake-up ===
# This line will only execute if somehow deep sleep fails
microcontroller.reset()
