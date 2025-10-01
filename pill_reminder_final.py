import time
import board
import analogio
import neopixel
import alarm
import microcontroller  # <- Needed for hard reset
from fade_controller import Fade_Controller


# === CONFIGURATION ===
NUM_PIXELS = 24
NEOPIXEL_PIN = board.A3
FSR_PIN = board.A0
BRIGHTNESS = 0.3
PIXEL_COLOR = (255, 0, 255, 0)

# Adjust these based on actual FSR readings
FSR_MAX_THRESHOLD = 11000  # Value above this = bottle removed
FSR_MIN_THRESHOLD = 4000   # Value below this = bottle replaced

# === NeoPixel Setup ===
pixels = neopixel.NeoPixel(
    NEOPIXEL_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=True,
    pixel_order=neopixel.GRBW  # RGBW-only
)

pixels.fill((0, 0, 0, 0))

fader = Fade_Controller(pixels, PIXEL_COLOR)


# === FSR Setup ===
fsr = analogio.AnalogIn(FSR_PIN)

def is_fsr_removed():
    avg = sum(fsr.value for _ in range(50)) // 50
    # print((avg,))
    return avg > FSR_MAX_THRESHOLD

def is_fsr_replaced():
    avg = sum(fsr.value for _ in range(50)) // 50
    return avg < FSR_MIN_THRESHOLD

# === 1. Wake up and light up reminder LEDs ===
print("Waking up... turning on reminder LEDs.")
  # Green for reminder
fader.fade_up()

# === 2. Wait for bottle to be removed ===
print("Waiting for bottle to be removed...")
while not is_fsr_removed():
    fader.fade_up()
    time.sleep(0.01)

print("Bottle removed.")

# === 3. Wait for bottle to stay removed for 3 full seconds ===
print("Monitoring for valid removal... must remain removed for 3 seconds.")

while True:
    # Wait for removal
    while not is_fsr_removed():
        time.sleep(0.01)
        fader.breath()

    removed_time = time.monotonic()

    while time.monotonic() - removed_time < 3:
        if is_fsr_replaced():
            print("Bottle returned too quickly. Resetting.")
            break  # Exit inner timer loop and restart removal check
        time.sleep(0.01)
        fader.breath()
    else:
        # The else block runs if the inner loop completes without a break
        print("Bottle stayed removed long enough. Proceeding.")
        break  # Exit the outer loop — valid removal confirmed

# === 4. Wait for bottle to be replaced ===
print("Waiting for bottle to be replaced...")
while not is_fsr_replaced():
    time.sleep(0.01)
    fader.breath()

# === 5. Turn off LEDs ===
print("Bottle replaced. Turning off LEDs.")
#pixels.fill((0, 0, 0, 0))  # Off
while not fader.is_finished():
    fader.fade_down()
    time.sleep(0.01)
# === 6. Sleep for 18 hours ===
SLEEP_TIME_SECONDS = 64800
print(f"Going to sleep for {SLEEP_TIME_SECONDS} seconds...")

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + SLEEP_TIME_SECONDS)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)

# === 7. Hard reset on wake-up ===
# This line will only execute if somehow deep sleep fails
microcontroller.reset()
# Write your code here :-)
