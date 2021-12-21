import time
from enum import Enum
from queue import Queue
from time import sleep

import cv2
import numpy as np
from djitellopy import Tello
from numpy import ndarray
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal

from map_matcher import SIFT_matcher
from utils.control import HiddenPrints
from match import draw


class ControlMode(Enum):
    SINGLE_MODE = 0
    RC_MODE = 1
    FIXED_MODE = 2


class FrameThread(QThread):
    signal = Signal()

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
        # self.template1 = cv2.imread("./output/oil.png")
        # self.template2 = cv2.imread("./output/oil1.png")
        # self.template3 = cv2.imread("./output/airplane.png")
        # self.template4 = cv2.imread("./output/airplane1.png")
        # self.template5 = cv2.imread("./output/airplane2.png")
        # self.template6 = cv2.imread("./output/airplane3.png")
        # self.template7 = cv2.imread("./output/airplane4.png")

    def run(self):
        while True:
            buffer = self.frame_read.frame
            self.img = cv2.flip(buffer, 0)
            #self.img = cv2.rotate(self.img, rotateCode=cv2.ROTATE_180)
            #self.img = self.img[::-1]
            # print(self.img)
            a = self.img*2
            # threshold = 0.79
            # draw(self.img, self.template1, threshold)
            # draw(self.img, self.template2, threshold)
            # draw(self.img, self.template3, threshold)
            # draw(self.img, self.template4, threshold)
            # draw(self.img, self.template5, threshold)
            # draw(self.img, self.template6, threshold)
            # draw(self.img, self.template7, threshold)
            self.signal.emit()
            sleep(0.02)


class ControlThread(QThread):
    finish_signal = Signal(int)

    def __init__(self, tello: Tello):
        super(ControlThread, self).__init__()
        self.tello = tello
        self.key = None

    def run(self):
        while True:
            # with HiddenPrints():
            #     self.tello.send_command_without_return("keepalive")
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
            else:
                sleep(0.01)


class MatchingThread(QThread):
    finish_signal = Signal()

    def __init__(self, frameThread: FrameThread, map: ndarray, nav_queue: Queue):
        super(MatchingThread, self).__init__()
        self.sift_matcher = SIFT_matcher(map)
        self.frameThread = frameThread

        self.result = None
        self.cx = 0
        self.cy = 0

        self.nav_queue = nav_queue

    def run(self):
        while True:
            if type(self.frameThread.img) == ndarray:
                try:
                    #start = time.perf_counter()

                    match_num, rectangle_degree, center = self.sift_matcher.match(
                        self.frameThread.img)
                    if center is not None and rectangle_degree > 0.6 and match_num>15:
                        self.cx, self.cy = center
                        self.nav_queue.put(center)

                    #end = time.perf_counter()
                    #print(rectangle_degree)
                    # print(end-start)
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
                self.pos[1]=-x
                self.pos[0]=-y+1280
                # print('2')
                # print(self.pos[0], self.pos[1])
                self.sift_signal.emit()
        
            sleep(0.02)
