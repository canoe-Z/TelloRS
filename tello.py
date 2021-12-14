from numpy import ndarray, source
from time import sleep
from djitellopy import Tello
#from MyTello import MyTello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal

from queue import Queue
import numpy as np
import cv2

from enum import Enum
from test_sift import match


class ControlMode(Enum):
    SINGLE_MODE = 0
    RC_MODE = 1
    FIXED_MODE = 2


class FrameThread(QThread):
    signal = Signal()

    def __init__(self, tello: Tello):
        super(FrameThread, self).__init__()

        self.tello = tello
        self.tello.connect()
        self.tello.streamon()
        self.frame_read = self.tello.get_frame_read()
        self.img = None

    def run(self):
        while True:
            # get a frame
            buffer = self.frame_read.frame
            self.img = cv2.flip(buffer, 0)
            a = self.img*2
            self.signal.emit()


class ControlThread(QThread):
    finish_signal = Signal(int)

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
                self.finish_signal.emit(self.key)
                self.key = None
            sleep(0.1)


class MatchingThread(QThread):
    finish_signal = Signal()

    def __init__(self, frameThread: FrameThread, source: ndarray):
        super(MatchingThread, self).__init__()
        self.source = source
        self.frameThread = frameThread
        self.result = None

    def run(self):
        while True:
            if type(self.frameThread.img) == ndarray:
                try:
                    tmp = np.copy(self.source)
                    self.result = match(self.frameThread.img, tmp)
                    self.finish_signal.emit()
                except:
                    print('定位失败')

            sleep(0.1)
