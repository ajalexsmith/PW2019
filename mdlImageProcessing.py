import sys, clsDrive
from time import sleep
import threading

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
        pixy.set_lamp(1, 0)
        blocks = BlockArray(100)
        while not self._stopevent.isSet(  ):
            count = pixy.ccc_get_blocks(100, blocks)
            if count > 0:
                for index in range(0, count):
                    curBlock = blocks[index]
                    if curBlock.m_signature == 1:
                        control.maze(curBlock.m_x, curBlock.m_y)
                        if control.stop == False:
                            print(control.angle)

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        pixy.set_lamp(0, 0)
        threading.Thread.join(self, timeout)

class Nebula(threading.Thread):

    def __init__(self, name='TestThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event(  )
        self._sleepperiod = 1.0

        threading.Thread.__init__(self, name=name)

    def run(self):
        pixy.init()
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

    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        pixy.set_lamp(0, 0)
        drive = clsDrive.Drive()
        drive.stop()
        threading.Thread.join(self, timeout)