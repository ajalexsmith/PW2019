from gfxhat import touch, lcd, backlight, fonts
import mdlDisplay, clsSettings


class clsGFX:
    def __init__(self):
        self.r = clsSettings.r
        self.g = clsSettings.g
        self.b = clsSettings.b
        self.image = None
        self.settings = clsSettings.Settings()

    def display(self):
        if self.image != None:
            newImage = mdlDisplay.rotateImage(self.image, 180)
            for x in range(128):
                for y in range(64):
                    pixel = newImage.getpixel((x, y))
                    lcd.set_pixel(x, y, pixel)
            lcd.show()

    def backlightSet(self):
        for x in range(6):
            backlight.set_pixels(x, self.settings.r, self.settings.g, self.settings.b)
        backlight.show()

    def off(self):
        for x in range(6):
            backlight.set_pixel(x, 0, 0, 0)
            touch.set_led(x, 0)
        backlight.show()
        lcd.clear()
        lcd.show()