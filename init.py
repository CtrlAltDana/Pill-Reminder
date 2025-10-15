import os
import board
import analogio
import neopixel


 
def get_neopixel(pin_str, num_pixels, brigthness):
    pin = getattr(board, pin_str)
    pixels = neopixel.NeoPixel(pin, num_pixels, brightness=0.5, auto_write=True, pixel_order=neopixel.GRB)
    pass
