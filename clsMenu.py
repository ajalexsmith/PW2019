import clsGFX, mdlDisplay

class Menu:
    '''

    Menu commands

    '''

    def __init__(self):
        self.options = {
            [mdlDisplay.blastOff, startBalastOff],
            [mdlDisplay.hubble, drive],
            [mdlDisplay.SpaceInvaders, drive],
            [mdlDisplay.PiNoon, drive],
            [mdlDisplay.COM, drive],
            [mdlDisplay.SOC, drive],
            [mdlDisplay.drive, drive],
            [mdlDisplay.settings, drive],
            [mdlDisplay.poweroff, poweroff],
            [mdlDisplay.reboot, reboot]
        }
        self.curPos = 0
        self.gfx = clsGFX()

    def nextOption(self):
        if self.curpos == len(self.options):
            self.curPos = 0
        else:
            self.curPos += 1

    def prevOption(self):
        if self.curpos -1 < 0:
            self.curPos = len(self.options) - 1
        else:
            self.curPos -= 1

    def updateDisplay(self):
        image = mdlPreFlight.PreFlight()
        image = self.options[0](image)
        self.gfx.image = image
        self.gfx.display()

    def Run(self):
        print("Add run code here")

    '''
    
    Process commands
    
    '''

menu = Menu()
menu.Run()
