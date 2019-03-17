import sys, clsDrive


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

def lineFollow:
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

def Maze():
    drive = clsDrive.Drive()
    control = clsDrive.Control()
    point = 0
    pixy.init()
    pixy.change_prog("color_connected_components");
    blocks = BlockArray(100)
    while 1:
        count = pixy.ccc_get_blocks(100, blocks)

        if count > 0:
            print
            'frame %3d:' % (frame)
            frame = frame + 1
            for index in range(0, count):
                curBlock = blocks[index]
                if curBlock.m_signature == 1:
                    con



                print
                '[BLOCK: SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (
                blocks[index].m_signature, blocks[index].m_x, blocks[index].m_y, blocks[index].m_width,
                blocks[index].m_height)
