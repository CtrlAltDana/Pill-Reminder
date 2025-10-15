import time
import math


class Fade_Controller:
    direction = "UP"

    def __init__(self, pixels, color, refresh=15, duration=300):
        self.pixels = pixels
        self.refresh = refresh  # time between refreshes in ms
        self.color = color
        self.increment = get_increment(color, refresh, duration)
        self.duration = duration
        self.prev_update_time = 0

    def _refresh_threhold_passed(self):
        time_passed = time.monotonic() - self.prev_update_time
        if time_passed > self.refresh / 1000:
            return True
        else:
            return False

    def _set(self, color):
        self.pixels.fill(color)
        self.prev_update_time = time.monotonic()

    def fade_up(self):
        if not self._refresh_threhold_passed():
            return
        self.direction = "UP"

        color = tuple(
            math.ceil(self.pixels[0][i] + self.increment[i])
            if self.pixels[0][i] + self.increment[i] < self.color[i]
            else self.color[i]
            for i in range(len(self.pixels[0]))
        )
        self._set(color)

    def fade_down(self, min_brightness = 0):
        if not self._refresh_threhold_passed():
            return
        self.direction = "DOWN"
        color = tuple(
            math.floor(self.pixels[0][i] - self.increment[i])
            if self.pixels[0][i] - self.increment[i] > self.color[i] * min_brightness
            else self.color[i] * min_brightness
            for i in range(len(self.pixels[0]))
        )
        self._set(color)

    def breath(self, min_brightness = .05):
        if not self._refresh_threhold_passed():
            return
        if self.pixels[0] == self.color:
            self.direction = "DOWN"
        if self.pixels[0] == tuple(int(x * min_brightness) for x in self.color):
            self.direction = "UP"
        if self.direction == "UP":
            self.fade_up()
        if self.direction == "DOWN":
            self.fade_down(min_brightness)

    def is_finished(self):
        if self.direction == "UP":
            return self.pixels[0] == self.color
        if  self.direction == "DOWN":
            return max(self.pixels[0]) == 0

def get_increment(color, refresh, duration):
    increments = abs(duration / refresh)
    return tuple(c / increments for c in color)
