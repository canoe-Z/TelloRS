from time import sleep
from djitellopy import Tello
#from MyTello import MyTello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal

from queue import Queue


class FrameThread(QThread):
    signal = Signal()

    def __init__(self, tello: Tello):
        super(FrameThread, self).__init__()

        self.tello = tello
        self.tello.connect()
        self.tello.streamon()
        self.frame_read = self.tello.get_frame_read()

    def run(self):
        while True:
            # get a frame
            self.img = self.frame_read.frame
            # print(self.img)
            a = self.img*2
            self.signal.emit()


class ControlThread(QThread):
    signal = Signal(int)

    def __init__(self, tello: Tello, queue: Queue):
        super(ControlThread, self).__init__()
        self.tello = tello
        self.queue = queue
        self.key = None

    def run(self):
        while True:
            if self.key:
                if self.key == Qt.Key_T:
                    self.tello.takeoff()
                if self.key == Qt.Key_W:
                    self.tello.move_forward(30)
                if self.key == Qt.Key_A:
                    self.tello.move_left(30)
                if self.key == Qt.Key_S:
                    self.tello.move_back(30)
                if self.key == Qt.Key_D:
                    self.tello.move_right(30)
                if self.key == Qt.Key_L:
                    self.tello.land()
                    # self.signal_land(emit)
                self.signal.emit(self.key)
                self.key = None
            sleep(0.1)


# def rc_control(tello: Tello, event: QtGui.QKeyEvent):
