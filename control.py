import time
from enum import Enum
from queue import Queue
from time import sleep

import cv2
import numpy as np
from djitellopy import Tello
from numpy import ndarray
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal, QMutex, QSemaphore

from match.sift_matcher import SIFTMatcher
from utils.control import HiddenPrints


class MyTello(Tello):
    # RETRY_COUNT = 3  # number of retries after a failed command
    # TELLO_IP = '192.168.10.1'  # Tello IP address

    # def __init__(self):
    #     super(MyTello,self).__init__(
    #         self,
    #         host='192.168.10.1',
    #         retry_count=3)

    def rc_control_by_key(self, key: int, move_speed: int):
        if key == Qt.Key_W:
            self.send_rc_control(0, move_speed, 0, 0)
        if key == Qt.Key_A:
            self.send_rc_control(-move_speed, 0, 0, 0)
        if key == Qt.Key_S:
            self.send_rc_control(0, -move_speed, 0, 0)
        if key == Qt.Key_D:
            self.send_rc_control(move_speed, 0, 0, 0)


class ControlMode(Enum):
    SINGLE_MODE = 0
    RC_MODE = 1
    FIXED_MODE = 2


class FrameThread(QThread):
    signal = Signal()
    qmut = QMutex()

    def __init__(self, tello: Tello):
        super(FrameThread, self).__init__()

        self.tello = tello
        self.img = None

        self.tello.connect()
        tello.set_video_bitrate(Tello.BITRATE_3MBPS)
        tello.set_video_resolution(Tello.RESOLUTION_720P)
        tello.set_video_fps(Tello.FPS_30)

        self.tello.streamon()
        self.frame_read = self.tello.get_frame_read()

    def run(self):
        while True:
            buffer = self.frame_read.frame
            buffer = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)
            self.qmut.lock()
            self.img = cv2.flip(buffer, 0)
            #a = self.img*2
            self.qmut.unlock()
            self.signal.emit()
            sleep(0.01)


class ControlThread(QThread):
    finish_signal = Signal(int)
    qmut = QMutex()

    def __init__(self, tello: Tello):
        super(ControlThread, self).__init__()
        self.tello = tello
        self.key = None

    def run(self):
        while True:
            self.qmut.lock()
            key = self.key
            self.qmut.unlock()
            if key:
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

                self.finish_signal.emit(key)
                self.qmut.lock()
                self.key = None
                self.qmut.unlock()
            sleep(0.01)
