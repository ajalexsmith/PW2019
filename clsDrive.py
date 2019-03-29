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
        self.TB1.i2cAddress = 10
        self.TB1.Init()
        self.TB2 = ThunderBorg.ThunderBorg()
        self.TB2.i2cAddress = 11
        self.TB2.Init()

    def drive(self):
        self.TB1.SetMotor1(self.m3)
        self.TB2.SetMotor2(self.m2)
        self.TB2.SetMotor1(self.m1)

    def driveWithSpeed(self):
        self.TB1.SetMotor1(self.m3 *  self.speed)
        self.TB2.SetMotor2(self.m2 *  self.speed)
        self.TB2.SetMotor1(self.m1 *  self.speed)

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

    def joltLeft(self):
        self.m1 = -0.5
        self.m2 = -0.5
        self.m3 = -0.5
        self.drive()
        time.sleep(0.01)
        self.stop()

    def turnLeft(self):
        self.m1 = -0.5
        self.m2 = -0.5
        self.m3 = -0.5
        self.drive()
        time.sleep(0.45)
        self.stop()

    def turnRight(self):
        self.m1 = 0.5
        self.m2 = 0.5
        self.m3 = 0.5
        self.drive()
        time.sleep(0.5)
        self.stop()

    def joltRight(self):
        self.m1 = 0.5
        self.m2 = 0.5
        self.m3 = 0.5
        self.drive()
        time.sleep(0.01)
        self.stop()

    def HarDrive(self, controlMeth):
        if controlMeth.stop:
            self.stop()
        else:
            #print("Drive")
            self.speed = controlMeth.speed
            val = 0.0166666666667
            if controlMeth.angle >= 0 and controlMeth.angle < 60:
                dif = controlMeth.angle
                self.m1 = 1
                self.m2 = -1 + (dif * val)
                self.m3 = 0 - (dif * val)
            elif controlMeth.angle >= 60 and controlMeth.angle < 120:
                dif = controlMeth.angle - 60
                self.m1 = 1 - (dif * val)
                self.m2 = 0 + (dif * val)
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
                dif = controlMeth.angle - 180
                self.m1 = -1 + (dif * val)
                self.m2 = 0 - (dif * val)
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
        #self.TOF.open()
        #self.distance = 1000

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
            print(str(self.angle))
            if self.speed < 0.2:
                self.stop = True

    def lineFollow(self, x1, y1, x2, y2):

        if x1 <= 24:
            #drive.joltRight()
            self.frame = 0
        elif x1 >= 53:
            # drive.joltLeft()
            self.frame = 2
        else:
            self.frame = 1

    def DriveToTarget(self, x, y):
        drive = Drive()
        dist = 158 - x
        if abs(dist) > 50:
            self.stop = True
            if dist > 50:
                drive.joltLeft()
            else:
                drive.joltRight()
        else:
            self.stop = False
            if dist > 25:
                self.angle = 20
            elif dist < -25:
                self.angle = 340
            elif dist > 15:
                self.angle = 10
            elif dist < -15:
                self.angle = 350
            else:
                self.angle = 0
            self.speed = 1

    def neb(self, x, y):
        self.distance = self.TOF.get_distance()
        print(str(self.distance))
        if self.distance >= 100:
            self.stop = False
            self.DriveToTarget(x, y)
        else:
            self.stop = True


    def maze(self, x, y, width):
        if x <= 125: #125:
            self.frame = 0
        elif x >= 189: # 189
            self.frame = 2
        else:
            self.frame = 1
        if width > 105:
            self.stop = True
            print("Stop")
        else:
            self.stop = False


            #315 157


        print(str(width))


        '''
        forward
        turn 90 degrees ACW
        Straight
        270 degrees until 3 seconds after seeing wall
        forwards till target
        90 degrees until no longer at wall
        forward till target
        90 ACW
        FORWARD TILL  TARGET


        self.distance = self.TOF.get_distance()
        self.TOF.stop_ranging()

        if self.progress == 0 or self.progress == 1 or self.progress == 3 or self.progress == 5 or self.progress == 6:
            if self.distance < 50:
                if self.progress == 0 or self.progress == 5:
                    Drive.spinRight()
                    time.sleep(1)
                    Drive.stop()
                    self.stop = True
                else:
                    self.stop = True

                self.progress += 1

            self.DriveToTarget(x, y)
        elif self.progress == 2 or self.progress == 7:
            #CHECK DISTANCE
            self.angle = 270
            self.speed = 1
        elif self.progress == 4:
            self.angle = 90
            self.speed = 0
        elif self.progress == 8:
            self.angle = 0
            self.speed = 1
            Drive.drive()
            time.sleep(1.5)
            Drive.stop()
            self.progress =+ 1
            self.stop = True



        if self.distance < 50 and (self.progress == 0 or self.progress == 1 or self.progress == 5):
            self.progress += 1
            self.distance = 1000
            print("Turning 90°")
        elif self.distance < 50 and self.progress == 3:
            self.progress += 1
            self.distance = 1000
        elif self.progress == 0 or self.progress == 1 or self.progress == 3 or self.progress == 5:
            self.distance -= 1
            self.DriveToTarget(x,y)

        elif self.progress == 2:
            if self.distance < 100:
                self.angle = 270
                self.speed = 1
            else:
                time.sleep(2)
                self.stop = True
                self.progress += 1

        elif self.progress == 4:
            if self.distance < 100:
                self.angle = 90
                self.speed = 1
            else:
                time.sleep(2)
                self.stop = True
                self.progress += 1

        else:
            print("Stop")

'''





