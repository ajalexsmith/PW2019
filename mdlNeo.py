# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import threading

class neo(threading.Thread):

    def __init__(self, name='TestThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event(  )
        self._sleepperiod = 1.0
        self.pixel_pin = board.D18
        self.num_pixels = 60

        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        self.ORDER = neopixel.GRB

        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.1, auto_write=False,
                                   pixel_order=self.ORDER)


        threading.Thread.__init__(self, name=name)

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.ORDER == neopixel.RGB or self.ORDER == neopixel.GRB else (r, g, b, 0)

    def rainbow_cycle(self, wait):
        for j in range(255):
            if self._stopevent.isSet(  ):
                break
                j = 244
                self.off()
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def run(self):
        while not self._stopevent.isSet(  ):
            self.rainbow_cycle(0.01)
        self.off()

    def off(self):
        for i in range(self.num_pixels):
            self.pixels[i] = (0,0,0)
        self.pixels.show()

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)


