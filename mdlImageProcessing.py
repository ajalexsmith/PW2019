import sys, clsDrive
from time import sleep
import threading
import VL53L1X
class TestThread(threading.Thread):

    def __init__(self, name='TestThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event(  )
        self._sleepperiod = 1.0

        threading.Thread.__init__(self, name=name)

    def run(self):
        """ main control loop """
        print("%s starts" % (self.getName(  ),))

        count = 0
        while not self._stopevent.isSet(  ):
            count += 1
            print("loop %d" % (count,))

        print("%s ends" % (self.getName(  ),))

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)

sys.path.insert(0, 'pixy2/build/python_demos')
import pixy
from ctypes import *
from pixy import *

class Blocks (Structure):
  _fields_ = [ ("m_signature", c_uint),
    ("m_x", c_uint),
    ("m_y", c_uint),
    ("m_width", c_uint),
    ("m_height", c_uint),
    ("m_angle", c_uint),
    ("m_index", c_uint),
    ("m_age", c_uint) ]


class Vector(Structure):
    _fields_ = [
        ("m_x0", c_uint),
        ("m_y0", c_uint),
        ("m_x1", c_uint),
        ("m_y1", c_uint),
        ("m_index", c_uint),
        ("m_flags", c_uint)]


class IntersectionLine(Structure):
    _fields_ = [
        ("m_index", c_uint),
        ("m_reserved", c_uint),
        ("m_angle", c_uint)]
'''
def lineFollow():
    drive = clsDrive.Drive()
    control = clsDrive.Control()
    pixy.init()
    pixy.set_lamp(1, 0)
    pixy.set_servos(500, 1000)

    vectors = VectorArray(100)
    intersections = IntersectionLineArray(100)
    frame = 0

    while 1:
        line_get_all_features()
        i_count = line_get_intersections(100, intersections)
        v_count = line_get_vectors(100, vectors)

        if i_count > 0 or v_count > 0:
            # print('frame %3d:' % (frame))
            frame = frame + 1
            for index in range(0, v_count):
                control.LineFollow(vectors[index].m_x0, vectors[index].m_y0, vectors[index].m_x1, vectors[index].m_y1)
'''

class LineFollow(threading.Thread):

    def __init__(self, name='TestThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event(  )
        self._sleepperiod = 1.0

        threading.Thread.__init__(self, name=name)

    def run(self):
        drive = clsDrive.Drive()
        control = clsDrive.Control()
        pixy.init()
        pixy.change_prog("line")

        pixy.set_servos(500, 800)
        pixy.set_lamp(1, 0)

        vectors = VectorArray(100)
        intersections = IntersectionLineArray(100)

        while not self._stopevent.isSet():
            line_get_all_features()
            i_count = line_get_intersections(100, intersections)
            v_count = line_get_vectors(100, vectors)
            print("Scanning")
            if i_count > 0 or v_count > 0:
                # print('frame %3d:' % (frame))
                for index in range(0, v_count):
                    control.lineFollow(vectors[index].m_x0, vectors[index].m_y0, vectors[index].m_x1, vectors[index].m_y1)
                    print(str(control.frame))
                    if control.frame == 2:
                        drive.joltRight()
                    elif control.frame == 0:
                        drive.joltLeft()
                    else:
                        control.angle = 0
                        control.speed = 1
                        control.stop = False
                        drive.HarDrive(control)
            else:
                control.angle = 0
                control.speed = 0.3
                control.stop = False
                drive.HarDrive(control)
                drive.stop()


    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        pixy.set_lamp(0, 0)
        pixy.set_servos(500, 500)
        threading.Thread.join(self, timeout)
        drive = clsDrive.Drive()
        drive.stop()


class Maze(threading.Thread):

    def __init__(self, name='TestThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event(  )
        self._sleepperiod = 1.0

        threading.Thread.__init__(self, name=name)

    def run(self):
        drive = clsDrive.Drive()
        control = clsDrive.Control()
        point = 0
        pixy.init()
        pixy.change_prog("color_connected_components");
        pixy.set_lamp(0, 0)
        pixy.set_servos(500, 650)
        blocks = BlockArray(100)
        while not self._stopevent.isSet(  ):
            count = pixy.ccc_get_blocks(100, blocks)
            if count > 0:
                x = 0
                y = 0
                width = 0

                for index in range(0, count):
                    curBlock = blocks[index]
                    if curBlock.m_signature == 1 and curBlock.m_width  > width:
                        width = curBlock.m_width
                        x = curBlock.m_x
                        y = curBlock.m_y
                if width > 0:
                    control.maze(x, y, width)
                    if control.stop == True:
                        if control.progress == 0 or control.progress == 1 or control.progress == 4 or control.progress == 5 or control.progress == 6:
                            drive.turnLeft()
                        elif control.progress == 2 or control.progress == 3 or control.progress == 7:
                            drive.turnRight()
                        control.progress += 1
                    elif control.frame == 2:
                        drive.joltRight()
                    elif control.frame == 0:
                        drive.joltLeft()
                    else:
                        control.angle = 0
                        control.speed = 0.7
                        control.stop = False
                        drive.HarDrive(control)
                else:
                    control.angle = 0
                    control.speed = 0.3
                    control.stop = False
                    drive.HarDrive(control)
            else:
                control.angle = 0
                control.speed = 0.3
                control.stop = False
                drive.HarDrive(control)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        pixy.set_lamp(0, 0)
        pixy.set_servos(500, 500)
        threading.Thread.join(self, timeout)
        drive = clsDrive.Drive()
        drive.stop()

class Nebula(threading.Thread):

    def __init__(self, name='TestThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event(  )
        self._sleepperiod = 1.0

        threading.Thread.__init__(self, name=name)

    def run(self):
        '''pixy.init()
        pixy.change_prog("color_connected_components");
        pixy.set_lamp(1, 0)
        drive = clsDrive.Drive()
        control = clsDrive.Control()
        blocks = BlockArray(100)
        while not self._stopevent.isSet(  ):
            count = pixy.ccc_get_blocks(100, blocks)
            if count > 0:
                for index in range(0, count):
                    curBlock = blocks[index]
                    print("x " + str(curBlock.m_x) + "- y " + str(curBlock.m_y))
                    #control.neb(curBlock.m_x, curBlock.m_y)
                    #control.speed = 0.5
                    #drive.HarDrive(control)
            else:
                #drive.joltLeft()
                print("Jolt")
        '''

        tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        tof.open()  # Initialise the i2c bus and configure the sensor
        tof.start_ranging(1)  # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range

        drive = clsDrive.Drive()
        control = clsDrive.Control()
        control.progress = 2
        pixy.init()
        pixy.change_prog("color_connected_components");
        pixy.set_lamp(0, 0)
        pixy.set_servos(500, 650)
        blocks = BlockArray(100)
        while not self._stopevent.isSet():
            count = pixy.ccc_get_blocks(100, blocks)
            if count > 0 and control.progress < 6:
                x = 0
                y = 0
                width = 0

                for index in range(0, count):
                    curBlock = blocks[index]
                    if curBlock.m_signature == control.progress and curBlock.m_width > width:
                        width = curBlock.m_width
                        x = curBlock.m_x
                        y = curBlock.m_y
                if width > 0:
                    control.distance = tof.get_distance()

                    #print(str(control.distance))
                    if control.distance < 100:
                        if control.progress == 5:
                            drive.stop()
                        else:
                            control.angle = 180
                            control.speed = 0.5
                            control.stop = False
                            drive.HarDrive(control)
                            sleep(1)
                            drive.stop()
                            control.progress += 1
                    else:
                        #print("control.neb")
                        print(str(width))
                        control.neb(x, y, width)
                        #print(str(control.frame))
                        if control.frame == 2:
                            drive.joltRight()
                        elif control.frame == 0:
                            drive.joltLeft()
                        else:
                            control.angle = 0
                            control.speed = 0.5
                            control.stop = False
                            drive.HarDrive(control)
                else:
                    drive.joltLeft()
            elif control.progress == 6:
                drive.stop()
                break
            else:
                drive.joltLeft()
        tof.close()




    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        pixy.set_lamp(0, 0)
        drive = clsDrive.Drive()
        drive.stop()
        threading.Thread.join(self, timeout)