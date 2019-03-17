from gfxhat import touch, lcd, backlight, fonts
import mdlDisplay, clsSettings


class clsGFX:
    def __init__(self):
        self.settings = clsSettings.Settings()
        self.image = None
        self.backlightSet()


    def display(self):
        if self.image != None:
            newImage = mdlDisplay.rotateImage(self.image, 180)
            for x in range(128):
                for y in range(64):
                    pixel = newImage.getpixel((x, y))
                    lcd.set_pixel(x, y, pixel)
            lcd.show()

    def backlightSet(self):
        backlight.set_all(self.settings.blR, self.settings.blG, self.settings.blB)
        backlight.show()

    def off(self):
        for x in range(6):
            backlight.set_all(0, 0, 0)
            touch.set_led(x, 0)
        backlight.show()
        lcd.clear()
        lcd.show()