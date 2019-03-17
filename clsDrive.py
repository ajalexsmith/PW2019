import ThunderBorg3 as ThunderBorg
import math, time
import VL53L1X
class Drive():
    def __init__(self):
        self.m1 = 0.0
        self.m2 = 0.0
        self.m3 = 0.0
        self.speed = 0.0
        self.TB1 = ThunderBorg.ThunderBorg()
        self.TB1.i2cAddress = 11
        self.TB1.Init()
        self.TB2 = ThunderBorg.ThunderBorg()
        self.TB2.i2cAddress = 10
        self.TB2.Init()

    def drive(self):
        self.TB1.SetMotor1(self.m1)
        self.TB2.SetMotor2(self.m2)
        self.TB2.SetMotor1(self.m3)

    def driveWithSpeed(self):
        self.TB1.SetMotor1(self.m1 * self.speed)
        self.TB2.SetMotor2(self.m2 * self.speed)
        self.TB2.SetMotor1(self.m3 * self.speed)

    def stop(self):
        self.m1 = 0.0
        self.m2 = 0.0
        self.m3 = 0.0
        self.drive()

    def spinLeft(self):
        self.m1 = -1
        self.m2 = -1
        self.m3 = -1
        self.drive()

    def spinRight(self):
        self.m1 = 1
        self.m2 = 1
        self.m3 = 1
        self.drive()

    def joltleft(self):
        self.m1 = -1
        self.m2 = -1
        self.m3 = -1
        self.drive()
        time.sleep(0.25)
        self.stop()

    def HarDrive(self, controlMeth):
        if controlMeth.stop:
            self.stop()
        else:
            self.speed = controlMeth.speed
            val = 0.0166666666667
            if controlMeth.angle >= -1 and controlMeth.angle < 60:
                dif = controlMeth.angle
                self.m1 = 1
                self.m2 = -1 + (dif * val)
                self.m3 = 0 - (dif * val)
            elif controlMeth.angle >= 60 and controlMeth.angle < 120:
                self.m1 = 1
                self.m2 = 0
                self.m3 = -1
            elif controlMeth.angle >= 120 and controlMeth.angle < 180:
                dif = controlMeth.angle - 120
                self.m1 = 0 - (dif * val)
                self.m2 = 1
                self.m3 = -1 + (dif * val)
            elif controlMeth.angle >= 180 and controlMeth.angle < 240:
                dif = controlMeth.angle - 180
                self.m1 = -1
                self.m2 = 1 - (dif * val)
                self.m3 = 0 + (dif * val)
            elif controlMeth.angle >= 240 and controlMeth.angle < 300:
                self.m1 = -1
                self.m2 = 0
                self.m3 = 1
            elif controlMeth.angle >= 300 and controlMeth.angle <= 360:
                dif = controlMeth.angle - 300
                self.m1 = 0 + (dif * val)
                self.m2 = -1
                self.m3 = 1 - (dif * val)
            self.driveWithSpeed()

class Control():
    def __init__(self):
        self.angle = 0
        self.speed = 0.0
        self.stop = False
        self.frame = 1 # 0 - left, 1 - Center, 2 - right
        self.distFromCenter = 0
        self.progress = 0
        self.TOF = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)

    def calcControl(self, x, y):
        if abs(x) < 0.2 and abs(y) < 0.2:
            self.stop = True
        else:
            self.stop = False

        if x > 0.0 and y == 0.0:
            self.angle = 90
        elif x == 0.0 and y < 0.0:
            self.angle = 180
        elif x < -0.0 and y == 0.0:
            self.angle = 270
        elif x == 0.0 and y > 0.0:
            self.angle = 0
        else:
            self.angle = math.degrees(math.atan(abs(y) / abs(x)))
            self.angle = int(5 * round(float(self.angle) / 5))

            if x > 0.0 and y > 0.0:
                self.angle = 90 - self.angle
            elif x > 0.0 and y < 0.0:
                self.angle = 90 + self.angle
            elif x < 0.0 and y < 0.0:
                self.angle = 270 - self.angle
            elif x < 0.0 and y > 0.0:
                self.angle = 270 + self.angle
        self.speed = min(math.sqrt((x * x) + (y * y)), 1)
        if self.speed < 0.2:
            self.stop = True

    def lineFollow(self, x1, y1, x2, y2):
        self.calcControl((x1-x2), (y1-y2))
        if x1 <= 24:
            self.frame = 0
        elif x1 >= 53:
            self.frame = 2
        else:
            self.frame = 1

        self.distFromCenter = abs(39 - x1)

    def maze(self, x, y):
        self.TOF.open()
        self.TOF.start_ranging(1)
        self.distance = self.TOF.get_distance()
        self.TOF.stop_ranging()
        self.calcControl(158 - x, y)
        print(self.angle)


