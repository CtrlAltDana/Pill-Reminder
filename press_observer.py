import time

class Press_Duration_Observer:
    press_started = False
    start_time = None
    values = [0]
    def __init__(self, duration, threshold):
        self.duration = duration
        self.threshold = threshold

    def _start(self):
        self.start_time = time.monotonic()
        self.press_started = True

    def update(self, value):
        if not self.press_started and value > self.threshold:
            self.press_started = True
            self.start_time = time.monotonic()
        if self.press_started:
            self.values.insert(0, value)

    def duration_passed(self):
        if self.press_started and min(self.values) > self.threshold:
            if time.monotonic() - self.start_time > self.duration:
                return True
        else:
            self.reset()
        #return False

    def reset(self):
        self.press_started = False
        self. values = []

