from numpy import ndarray, source
from time import sleep
from djitellopy import Tello
#from MyTello import MyTello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal

from queue import Queue
import numpy as np
import cv2
import time
from enum import Enum
from test_sift import match

#from icecream import ic


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
        tello.set_video_bitrate(Tello.BITRATE_3MBPS)
        tello.set_video_resolution(Tello.RESOLUTION_720P)
        tello.set_video_fps(Tello.FPS_30)

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
        self.cx = 0
        self.cy = 0

    def run(self):
        while True:
            if type(self.frameThread.img) == ndarray:
                try:
                    tmp = np.copy(self.source)
                    self.cx, self.cy = match(self.frameThread.img, tmp)
                    # self.finish_signal.emit()
                except:
                    pass
                    # print('定位失败')

            sleep(0.1)


class IMUThread(QThread):
    imu_signal = Signal()

    def __init__(self, tello: Tello, source: ndarray):
        super(IMUThread, self).__init__()
        self.tello = tello
        self.source = source
        self.result = None
        self.last_time = time.time()
        self.pos = np.zeros(3, dtype=np.float32)
        #self.pos = np.array([0, 0, 0], dtype=np.float32)

    def run(self):
        while True:
            vx = -self.tello.get_speed_x()
            vy = self.tello.get_speed_y()
            vz = self.tello.get_speed_z()
            v = np.array([vx, vy, vz], dtype=np.float32)

            currnet_time = time.time()
            dt = currnet_time-self.last_time
            self.last_time = currnet_time

            ds = v*dt
            self.pos += ds*2.73*10
            print(self.pos[0], self.pos[1], self.pos[2])
            
            self.result = cv2.circle(
                self.source, (abs(int(self.pos[1])), 1280-abs(int(self.pos[0]))), 4, (0, 255, 255), 10)
            self.imu_signal.emit()
            sleep(0.1)
