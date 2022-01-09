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

from match.sift import SIFTMatcher
from utils.control import HiddenPrints
from vidgear.gears.stabilizer import Stabilizer


class ControlMode(Enum):
    SINGLE_MODE = 0
    RC_MODE = 1
    FIXED_MODE = 2


class FrameThread(QThread):
    signal = Signal()
    qmut = QMutex()
    stab = Stabilizer(smoothing_radius=7, border_size=0,
                      crop_n_zoom=False, border_type='reflect_101')

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

        self.stab_on = False

    def run(self):
        while True:
            buffer = self.frame_read.frame
            buffer = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)

            frame = cv2.flip(buffer, 0)

            if self.stab_on:
                # send current frame to stabilizer for processing
                stabilized_frame = self.stab.stabilize(frame)

                # wait for stabilizer which still be initializing
                if stabilized_frame is None:
                    continue

            self.qmut.lock()
            if self.stab_on:
                self.img = stabilized_frame
            else:
                self.img = frame

            # 虽然不知道有什么用，但是千万不要删这行代码
            a = self.img*2

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
        self.move_distance = 30
        self.tracking = False
        self.x_move = 0
        self.y_move = 0

    def run(self):
        while True:
            if not self.tracking:
                self.qmut.lock()
                key = self.key
                self.qmut.unlock()
                if key:
                    if key == Qt.Key_T:
                        self.tello.takeoff()
                    if key == Qt.Key_W:
                        self.tello.move_forward(self.move_distance)
                    if key == Qt.Key_A:
                        self.tello.move_left(self.move_distance)
                    if key == Qt.Key_S:
                        self.tello.move_back(self.move_distance)
                    if key == Qt.Key_D:
                        self.tello.move_right(self.move_distance)
                    if key == Qt.Key_L:
                        self.tello.land()

                    self.finish_signal.emit(key)
                    self.qmut.lock()
                    self.key = None
                    self.qmut.unlock()
                sleep(0.01)
            else:
                self.tello.send_rc_control(self.x_move, self.y_move, 0, 0)
                sleep(0.01)
