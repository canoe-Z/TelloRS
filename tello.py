from time import sleep
from djitellopy import Tello
#from MyTello import MyTello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal

from queue import Queue

import cv2


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
            #import numpy as np
            #self.img = np.ascontiguousarray(self.frame_read.frame[::-1])

            # self.img=self.img[::-1]
            # self.img=np.ascontiguousarray(self.img)
            #self.img = cv2.flip(self.img, 0)
            # self.img = cv2.rotate(cv2.flip(self.img, 1),
            #                       rotateCode=cv2.ROTATE_180)
            buffer = self.frame_read.frame
            self.img = cv2.flip(buffer, 0)
            #self.img = cv2.rotate(self.img, rotateCode=cv2.ROTATE_180)
            #self.img = self.img[::-1]
            # print(self.img)
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
                    # self.signal_land(emit)
                self.finish_signal.emit(self.key)
                self.key = None
            sleep(0.1)


# def rc_control(tello: Tello, event: QtGui.QKeyEvent):
