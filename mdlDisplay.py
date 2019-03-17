from gfxhat import lcd, fonts
from PIL import Image, ImageFont, ImageDraw
import mdlIcon
import subprocess as sp
import ThunderBorg3 as ThunderBorg

'''
Useful Functions
'''

def rotateImage(image, angle): #Rotates Image desired angle
    image = image.rotate(angle)
    return image

def addMenuText(image, text): # Adds text to menu
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fonts.PressStart2P, 10)

    w, h = font.getsize(text)

    x = (128 - w) // 2
    y = (64 - h)

    draw.text((x, y), text, 1, font)

    return image

'''
Preflight
'''

def PreFlight():
    image = mdlPil.creatImage()
    image = ControllerCheck(image)
    image = TBCheck(image)
    mdlGFX.gfxDisplay(image)

    return image



def ControllerCheck(image):
    stdoutdata = sp.getoutput("hcitool con")

    if "00:06:F7:13:66:8F" in stdoutdata.split():
        image = mdlPil.Controller(True, image)
    else:
        image = mdlPil.Controller(False, image)

    return image

def TBCheck(image):
    TB1 = ThunderBorg.ThunderBorg()
    TB1.i2cAddress = 10
    TB1.Init()
    image = mdlPil.TB(TB1.foundChip, image, 1)

    TB2 = ThunderBorg.ThunderBorg()
    TB2.i2cAddress = 11
    TB2.Init()
    image = mdlPil.TB(TB1.foundChip, image, 2)
    return image


'''
Menu Options
'''

def blastOff(image):
    draw = ImageDraw.Draw(image)
    draw.point(mdlIcon.BlastOff(), 1)
    addMenuText(image, "Blast Off")
    return image

def hubble(image):
    draw = ImageDraw.Draw(image)

    draw.point(mdlIcon.hubble(), 1)
    addMenuText(image, "Hubble")
    return image

def SpaceInvaders(image):
    draw = ImageDraw.Draw(image)

    draw.point(mdlIcon.SpaceInvaders(), 1)
    addMenuText(image, "Space Inv")
    return image

def PiNoon(image):
    draw = ImageDraw.Draw(image)

    draw.point(mdlIcon.noon(), 1)
    addMenuText(image, "PiNoon")
    return image

def COM(image):
    draw = ImageDraw.Draw(image)
    draw.point(mdlIcon.com(), 1)
    addMenuText(image, "C O M")

    return image

def SOC(image):
    draw = ImageDraw.Draw(image)
    draw.point(mdlIcon.soc(), 1)
    addMenuText(image, "Spirit Of Cur")

    return image

def drive(image):
    draw = ImageDraw.Draw(image)

    draw.ellipse([(41,7), (85,51)], 1, 1)
    draw.ellipse([(46,12), (80,46)], 0, 0)
    draw.ellipse([(58,24), (68,34)], 1, 1)
    draw.line([(45,27), (83,27)], 1, 1)
    draw.line([(45,28), (83,28)], 1, 1)
    draw.line([(45,29), (83,29)], 1, 1)

    draw.line([(62, 29), (62, 49)], 1, 1)
    draw.line([(63, 29), (63, 49)], 1, 1)
    draw.line([(64, 29), (64, 49)], 1, 1)

    addMenuText(image, "Drive")

    return image

def settings(image):
    draw = ImageDraw.Draw(image)
    draw.point(mdlIcon.settings(), 1)
    addMenuText(image, "Settings")

    return image

def poweroff(image):
    draw = ImageDraw.Draw(image)
    draw.point(mdlIcon.Shutdown(), 1)

    addMenuText(image, "Shutdown")

    return image

def reboot(image):
    draw = ImageDraw.Draw(image)
    draw.point(mdlIcon.restart(), 1)

    addMenuText(image, "Re-Boot")

    return image