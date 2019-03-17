import clsGFX, mdlDisplay, mdlImageProcessing
from gfxhat import touch, lcd, backlight
import signal
class Menu:
    '''

    Menu commands

    '''

    def __init__(self):
        self.options = [
            [mdlDisplay.blastOff, mdlImageProcessing.TestThread],
            [mdlDisplay.hubble, self.test],
            [mdlDisplay.SpaceInvaders, self.test],
            [mdlDisplay.PiNoon, self.test],
            [mdlDisplay.COM, self.test],
            [mdlDisplay.SOC, self.test],
            [mdlDisplay.drive, self.test],
            [mdlDisplay.settings, self.test],
            [mdlDisplay.poweroff, self.test],
            [mdlDisplay.reboot, self.test]
        ]
        self.curPos = 0
        self.gfx = clsGFX.clsGFX()
        self.InProgram = False
        self.curThread = None

    def nextOption(self):
        if self.curPos == len(self.options):
            self.curPos = 0
        else:
            self.curPos += 1
        self.updateDisplay()

    def prevOption(self):
        if self.curPos -1 < 0:
            self.curPos = len(self.options) - 1
        else:
            self.curPos -= 1
        self.updateDisplay()

    def updateDisplay(self):
        print("Update")
        image = mdlDisplay.PreFlight()
        image = self.options[self.curPos][0](image)
        self.gfx.image = image
        self.gfx.display()

    def test(self):
        global testthread
        testthread.start()

    '''
    
    Process commands
    
    '''

menu = Menu()
menu.updateDisplay()
def handler(ch, event):
    global menu
    if event == 'press':
        touch.set_led(ch, 1)
        if ch == 3:
            menu.nextOption()
        elif ch == 5:
            menu.prevOption()
        elif ch == 4:
            menu.curThread = menu.options[menu.curPos][1]()
            menu.curThread.start()
        elif ch == 0:
            menu.curThread.join()
        touch.set_led(ch, 0)
        print(str(menu.curPos))

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