import clsDrive
import threading
from approxeng.input.selectbinder import ControllerResource

class Drive(threading.Thread):

    def __init__(self, name='TestThread'):
        """ constructor, setting initial variables """
        self._stopevent = threading.Event(  )
        self._sleepperiod = 1.0

        threading.Thread.__init__(self, name=name)

    def run(self):
        drive = clsDrive.Drive()
        control = clsDrive.Control()
        while not self._stopevent.isSet():
            with ControllerResource() as joystick:
                print('Found a joystick and connected')
                while not self._stopevent.isSet():
                    control.calcControl(round(joystick.rx, 2), round(joystick.ry, 2))
                    drive.HarDrive(control)



    def join(self, timeout=None):
        """ Stop the thread. """
        self._stopevent.set(  )
        threading.Thread.join(self, timeout)