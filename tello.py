from time import sleep
from djitellopy import Tello
#from MyTello import MyTello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal

from queue import Queue
from match import draw

import cv2


class FrameThread(QThread):
    signal = Signal()

    def __init__(self, tello: Tello):
        super(FrameThread, self).__init__()

        self.tello = tello
        self.tello.connect()
        self.tello.streamon()
        self.frame_read = self.tello.get_frame_read()
        self.template1 = cv2.imread("./output/oil.png")
        self.template2 = cv2.imread("./output/oil1.png")
        self.template3 = cv2.imread("./output/airplane.png")
        self.template4 = cv2.imread("./output/airplane1.png")
        self.template5 = cv2.imread("./output/airplane2.png")
        self.template6 = cv2.imread("./output/airplane3.png")
        self.template7 = cv2.imread("./output/airplane4.png")

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
            #a = self.img*2
            threshold = 0.79
            draw(self.img,self.template1,threshold)
            draw(self.img,self.template2,threshold)
            draw(self.img,self.template3,threshold)
            draw(self.img,self.template4,threshold)
            draw(self.img,self.template5,threshold)
            draw(self.img,self.template6,threshold)
            draw(self.img,self.template7,threshold)

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
