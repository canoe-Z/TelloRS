import time
from enum import Enum
from queue import Queue
from time import sleep

import cv2
import numpy as np
from djitellopy import Tello
from numpy import ndarray
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal, QMutex

from match.sift_matcher import SIFTMatcher
from utils.control import HiddenPrints
from tello import FrameThread


class MatchingThread(QThread):
    finish_signal = Signal()

    def __init__(self, frameThread: FrameThread, map: ndarray, nav_queue: Queue):
        super(MatchingThread, self).__init__()
        self.sift_matcher = SIFTMatcher(map)
        self.frameThread = frameThread

        self.result = None
        self.cx = 0
        self.cy = 0

        self.nav_queue = nav_queue

    def run(self):
        while True:
            if type(self.frameThread.img) == ndarray:
                try:
                    match_num, rectangle_degree, center = self.sift_matcher.match(
                        self.frameThread.img)
                    if center is not None and rectangle_degree > 0.6 and match_num > 15:
                        self.cx, self.cy = center
                        self.nav_queue.put(center)

                    self.finish_signal.emit()
                except:
                    pass
                    # print('定位失败')
            sleep(0.05)


class IMUThread(QThread):
    imu_signal = Signal()
    sift_signal = Signal()

    def __init__(self, tello: Tello, nav_queue: Queue):
        super(IMUThread, self).__init__()
        self.tello = tello

        self.last_time = time.time()
        self.pos = np.zeros(3, dtype=np.float32)

        self.nav_queue = nav_queue

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
            #print(self.pos[0], self.pos[1], self.pos[2])
            if self.nav_queue.empty():
                # print('empty')
                # print(self.pos[0], self.pos[1], self.pos[2])
                self.imu_signal.emit()
            if not self.nav_queue.empty():
                x, y = self.nav_queue.get()
                self.pos[1] = -x
                self.pos[0] = -y+1280
                # print('2')
                # print(self.pos[0], self.pos[1])
                self.sift_signal.emit()

            sleep(0.02)
