from time import sleep
from djitellopy import Tello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal

from queue import Queue


class MyThread(QThread):
    signal = Signal()

    def __init__(self, tello: Tello):
        super(MyThread, self).__init__()

        self.tello = tello
        self.tello.connect()
        self.tello.streamon()
        self.frame_read = self.tello.get_frame_read()

    def run(self):
        while True:
            # get a frame
            self.img = self.frame_read.frame
            #print(self.img)
            a = self.img*2
            self.signal.emit()


class TestThread(QThread):
    signal = Signal()

    def __init__(self, tello: Tello, queue: Queue):
        super(TestThread, self).__init__()
        self.tello = tello
        self.queue = queue

    def run(self):
        while True:
            if self.queue.not_empty:
                key = self.queue.get()
                print(key)
                if key == Qt.Key_T:
                    self.tello.takeoff()
                if key == Qt.Key_W:
                    self.tello.move_forward(30)
                if key == Qt.Key_A:
                    self.tello.move_left(30)
                if key == Qt.Key_S:
                    self.tello.move_back(30)
                if key == Qt.Key_D:
                    self.tello.move_right(30)
                if key == Qt.Key_L:
                    self.tello.land()
            sleep(0.1)
