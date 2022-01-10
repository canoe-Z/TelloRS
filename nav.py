import math
import time
from queue import Queue
from time import sleep

import cv2
import numpy as np
from djitellopy import Tello
from numpy import ndarray
from PySide6.QtCore import QDateTime, QMutex, Qt, QThread, Signal
from simple_pid import PID

from control import FrameThread
from match.sift import SIFTMatcher

matching_flag = 0


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
                        global matching_flag
                        matching_flag += 1
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

    def __init__(self, tello: Tello, nav_queue: Queue, auto_queue: Queue):
        super(IMUThread, self).__init__()
        self.tello = tello

        self.last_time = time.time()
        self.pos = np.zeros(3, dtype=np.float32)

        self.nav_queue = nav_queue
        self.auto_queue = auto_queue

    def run(self):
        while True:
            vx = -self.tello.get_speed_x()
            vy = self.tello.get_speed_y()
            vz = self.tello.get_speed_z()
            v = np.array([vx, vy, vz], dtype=np.float32)

            currnet_time = time.time()
            dt = currnet_time-self.last_time
            self.last_time = currnet_time

            ds = -v*dt
            self.pos += ds*2.8*10
            if self.nav_queue.empty():
                # print('empty')
                # print(self.pos[0], self.pos[1], self.pos[2])
                self.imu_signal.emit()
            if not self.nav_queue.empty():
                x, y = self.nav_queue.get()
                dst = math.sqrt((self.pos[1]-(-x)) **
                                2+(self.pos[0]-(-y+1280))**2)
                if matching_flag == 1 or dst < 300:
                    self.pos[1] = -x
                    self.pos[0] = -y+1280
                # print('2')
                # print(self.pos[0], self.pos[1])
                self.sift_signal.emit()
            if not self.auto_queue.empty():
                self.auto_queue.get()
            self.auto_queue.put([-int(self.pos[1]), -int(self.pos[0])+1280])

            sleep(0.01)

    # def imu2img(self, x, y):
    #     return -y+1280, -x

    # def img2imu(self, x, y):
    #     return -x, -y+1280


class AutoFlightThread(QThread):
    finish_signal = Signal(int)

    def __init__(self, tello: Tello, auto_queue: Queue, frameThread: FrameThread):
        super(AutoFlightThread, self).__init__()
        self.tello = tello
        self.auto_queue = auto_queue
        self.frame_thread = frameThread

    def run(self):
        while True:
            x, y = self.auto_queue.get()
            print(x, y)
            if 100 < y < 1230 and 10 < x < 1260:
                self.tello.move_forward(30)
                curDataTime = QDateTime.currentDateTime().toString('hh-mm-ss-yyyy-MM-dd')
                cv2.imwrite('output/'+curDataTime +
                            '.png', self.frame_thread.img)
            if y < 100 and 10 < x < 1260:
                self.tello.move_right(50)
                curDataTime = QDateTime.currentDateTime().toString('hh-mm-ss-yyyy-MM-dd')
                cv2.imwrite('output/'+curDataTime +
                            '.png', self.frame_thread.img)
                self.tello.rotate_clockwise(180)
                self.tello.move_forward(50)
                curDataTime = QDateTime.currentDateTime().toString('hh-mm-ss-yyyy-MM-dd')
                cv2.imwrite('output/'+curDataTime +
                            '.png', self.frame_thread.img)
            if y > 1230 and 10 < x < 1260:
                self.tello.move_left(50)
                curDataTime = QDateTime.currentDateTime().toString('hh-mm-ss-yyyy-MM-dd')
                cv2.imwrite('output/'+curDataTime +
                            '.png', self.frame_thread.img)
                self.tello.rotate_clockwise(180)
                self.tello.move_forward(50)
                curDataTime = QDateTime.currentDateTime().toString('hh-mm-ss-yyyy-MM-dd')
                cv2.imwrite('output/'+curDataTime +
                            '.png', self.frame_thread.img)
            # else:
            #     self.tello.land()
            sleep(1)


class PointFlightThread(QThread):
    message_signal = Signal(str)

    def __init__(self, tello: Tello, auto_queue: Queue):
        super(PointFlightThread, self).__init__()
        self.tello = tello
        self.auto_queue = auto_queue

    def set_end_pos(self, x, y):
        self.setpoint_x = x
        self.setpoint_y = y
        self.pid_x = PID(3, 0.01, 0.01, setpoint=x)
        self.pid_y = PID(3, 0.01, 0.01, setpoint=y)
        self.pid_x.output_limits = (-15, 15)
        self.pid_y.output_limits = (-15, 15)

    def update(self, vx, vy):
        self.tello.send_rc_control(int(vx), int(vy), 0, 0)
        img_x, img_y = self.auto_queue.get()
        y = 1280-img_y
        x = img_x
        return x, y

    def run(self):
        x, y = self.auto_queue.get()
        while True:
            radius = 15
            if abs(x-self.setpoint_x) <= radius and abs(y-self.setpoint_y) <= radius:
                for _ in range(5):
                    self.tello.send_rc_control(0, 0, 0, 0)
                print("定点飞行结束")
                self.message_signal.emit("定点飞行结束")
                break
            else:
                vx = self.pid_x(x)
                vy = self.pid_y(y)
                print(x, y, vx, vy)
                x, y = self.update(vx, vy)
                self.message_signal.emit('{} {} {} {}'.format(x, y, vx, vy))

            sleep(0.02)
