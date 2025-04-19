import time
import board
import analogio
import neopixel
import alarm
import microcontroller  # <- Needed for hard reset

# === CONFIGURATION ===
NUM_PIXELS = 24
NEOPIXEL_PIN = board.A3
FSR_PIN = board.A0
BRIGHTNESS = 0.3

# Adjust these based on actual FSR readings
FSR_MAX_THRESHOLD = 11000  # Value above this = bottle removed
FSR_MIN_THRESHOLD = 9000   # Value below this = bottle replaced

# === NeoPixel Setup ===
pixels = neopixel.NeoPixel(
    NEOPIXEL_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=True,
    pixel_order=neopixel.GRB  # RGB-only
)

# === FSR Setup ===
fsr = analogio.AnalogIn(FSR_PIN)

def is_fsr_removed():
    avg = sum(fsr.value for _ in range(5)) // 5
    return avg > FSR_MAX_THRESHOLD

def is_fsr_replaced():
    avg = sum(fsr.value for _ in range(5)) // 5
    return avg < FSR_MIN_THRESHOLD

# === 1. Wake up and light up reminder LEDs ===
print("Waking up... turning on reminder LEDs.")
pixels.fill((0, 255, 0))  # Green for reminder

# === 2. Wait for bottle to be removed ===
print("Waiting for bottle to be removed...")
while not is_fsr_removed():
    time.sleep(0.1)

print("Bottle removed.")

# === 3. Pause before detecting return ===
time.sleep(3)

# === 4. Wait for bottle to be replaced ===
print("Waiting for bottle to be replaced...")
while not is_fsr_replaced():
    time.sleep(0.1)

print("Bottle replaced. Turning off LEDs.")
pixels.fill((0, 0, 0))  # Off

# === 5. Sleep for 18 hours ===
SLEEP_TIME_SECONDS = 64800
print(f"Going to sleep for {SLEEP_TIME_SECONDS} seconds...")

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + SLEEP_TIME_SECONDS)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)

# === 6. Hard reset on wake-up ===
# This line will only execute if somehow deep sleep fails
microcontroller.reset()
# Write your code here :-)
