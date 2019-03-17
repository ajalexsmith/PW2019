import clsGFX, mdlDisplay
from gfxhat import touch, lcd, backlight

class Menu:
    '''

    Menu commands

    '''

    def __init__(self):
        self.options = {
            [mdlDisplay.blastOff, self.test()],
            [mdlDisplay.hubble, self.test()],
            [mdlDisplay.SpaceInvaders, self.test()],
            [mdlDisplay.PiNoon, self.test()],
            [mdlDisplay.COM, self.test()],
            [mdlDisplay.SOC, self.test()],
            [mdlDisplay.drive, self.test()],
            [mdlDisplay.settings, self.test()],
            [mdlDisplay.poweroff, self.test()],
            [mdlDisplay.reboot, self.test()]
        }
        self.curPos = 0
        self.gfx = clsGFX()
        self.InProgram = False

    def nextOption(self):
        if self.curpos == len(self.options):
            self.curPos = 0
        else:
            self.curPos += 1
        self.updateDisplay

    def prevOption(self):
        if self.curpos -1 < 0:
            self.curPos = len(self.options) - 1
        else:
            self.curPos -= 1
        self.updateDisplay()

    def updateDisplay(self):
        image = mdlDisplay.PreFlight()
        image = self.[self.curPos][0](image)
        self.gfx.image = image
        self.gfx.display()

    '''
    
    Process commands
    
    '''

    def test(self):
        fram = 1
        while True:
            print(str(fram))
            fram =+ 1

menu = Menu()

def handler(ch, event):
    global menu
    if event == 'press':

        touch.set_led(ch, 1)
        if ch == 3:
            menu.nextOption()
        elif ch == 5:
            menu.prevOption()
        if ch == 4:
            print("Start")
        touch.set_led(ch, 0)

 for x in range(6):
        touch.on(x, handler)
    try:
        signal.pause()
    except KeyboardInterrupt:
        for x in range(6):
            backlight.set_pixel(x, 0, 0, 0)
            touch.set_led(x, 0)
        backlight.show()
        lcd.clear()
        lcd.show()