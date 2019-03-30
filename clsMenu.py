import clsGFX, mdlDisplay, mdlImageProcessing, clsDrive
import mdlControl, mdlNeo
from subprocess import call
from gfxhat import touch, lcd, backlight
import signal
from time import sleep
class Menu:
    '''

    Menu commands

    '''

    def __init__(self):
        self.options = [
            [mdlDisplay.blastOff, mdlImageProcessing.LineFollow, True],
            [mdlDisplay.hubble, mdlImageProcessing.Nebula, True],
            [mdlDisplay.SpaceInvaders, mdlControl.Drive, True],
            [mdlDisplay.PiNoon, mdlControl.Drive, True],
            [mdlDisplay.COM, mdlImageProcessing.Maze, True],
            [mdlDisplay.SOC, mdlControl.Drive, True],
            [mdlDisplay.drive, mdlControl.Drive, True],
            [mdlDisplay.LED, mdlNeo.neo, None],
            [mdlDisplay.testTurn, self.testTurn, False],
            [mdlDisplay.poweroff, self.poweroff, False],
            [mdlDisplay.reboot, self.reboot, False]
        ]
        self.curPos = 0
        self.gfx = clsGFX.clsGFX()
        self.InProgram = False
        self.curThread = None
        self.ledThread = None
        self.inThread = False
        self.toggleLed = False

    def nextOption(self):
        if self.curPos == len(self.options) - 1:
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

    def poweroff(self):
        for x in range(6):
            backlight.set_pixel(x, 0, 0, 0)
            touch.set_led(x, 0)
        backlight.show()
        lcd.clear()
        drive = clsDrive.Drive()
        drive.stop()
        lcd.show()
        call("sudo poweroff", shell=True)

    def testTurn(self):
        drive = clsDrive.Drive()
        drive.turnRight()
        sleep(2)
        drive.turnLeft()


    def reboot(self):
        for x in range(6):
            backlight.set_pixel(x, 0, 0, 0)
            touch.set_led(x, 0)
        backlight.show()
        lcd.clear()
        drive = clsDrive.Drive()
        drive.stop()
        lcd.show()
        call("sudo reboot", shell=True)
    '''
    
    Process commands
    
    '''

menu = Menu()
menu.updateDisplay()
def handler(ch, event):
    global menu
    if event == 'press':
        touch.set_led(ch, 1)
        if ch == 3 and menu.inThread == False:
            menu.nextOption()
        elif ch == 5 and menu.inThread == False:
            menu.prevOption()
        elif ch == 4 and menu.inThread == False:
            if menu.options[menu.curPos][2] == None:
                if menu.toggleLed:
                    print("Turning off")
                    menu.ledThread.join()
                    menu.toggleLed = False
                else:
                    print("Turning On")
                    menu.ledThread = menu.options[menu.curPos][1]()
                    menu.ledThread.start()
                    menu.toggleLed = True
            elif menu.options[menu.curPos][2] == True:
                menu.inThread = True
                menu.curThread = menu.options[menu.curPos][1]()
                menu.curThread.start()
            else:
                menu.options[menu.curPos][1]()
        elif ch == 0 and menu.inThread == True:
            menu.curThread.join()
            menu.inThread = False
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
    drive = clsDrive.Drive()
    drive.stop()
    lcd.show()