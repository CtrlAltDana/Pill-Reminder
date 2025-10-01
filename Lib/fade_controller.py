import time
import math


class Fade_Controller:
    direction = "UP"
    #current_color = (0, 0, 0, 0)

    def __init__(self, pixels, color, refresh=15, duration=1000):
        self.pixels = pixels
        self.refresh = refresh  # time between refreshes in ms
        self.color = color
        self.increment = get_RGBW_increment(color, refresh, duration)
        print(self.increment)
        self.duration = duration
        self.prev_update_time = 0

        #pixels.fill(self.current_color)

    def _refresh_threhold_passed(self):
        time_passed = time.monotonic() - self.prev_update_time
        if time_passed > self.refresh / 1000:
            return True
        else:
            return False

    def _set(self, color):
        self.pixels.fill(color)
        #self.current_color = color
        self.prev_update_time = time.monotonic()
        #print(color)

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
            return self.pixels[0] == (0, 0, 0, 0)


def get_RGBW_increment(color, refresh, duration):
    increments = abs(duration / refresh)
    print(increments)
    print(color[0] / increments)
    return (
        color[0] / increments,  # Red
        color[1] / increments,  # Green
        color[2] / increments,  # Blue
        color[3] / increments,  # White
    )
