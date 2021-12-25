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

from map_matcher import SIFT_matcher
from utils.control import HiddenPrints
from det.template import draw

from tello import FrameThread

from det.nanodet import NanoDet
from utils.control import HiddenPrints


class DetectThread(QThread):
    signal = Signal()
    mutex = QMutex()

    def __init__(self, frameThread: FrameThread):
        super(DetectThread, self).__init__()

        self.frameThread = frameThread
        self.frame = None

        self.template1 = cv2.imread("./output/oil.png")
        self.template2 = cv2.imread("./output/oil1.png")
        self.template3 = cv2.imread("./output/airplane.png")
        self.template4 = cv2.imread("./output/airplane1.png")
        self.template5 = cv2.imread("./output/airplane2.png")
        self.template6 = cv2.imread("./output/airplane3.png")
        self.template7 = cv2.imread("./output/airplane4.png")

        self.predictor = NanoDet()
        # predictor.set_target(0)

    def run(self):
        while True:
            self.mutex.lock()
            self.frame = self.frameThread.img
            self.mutex.unlock()
            #frame = cv2.flip(buffer, 0)
            #frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_180)
            #frame = frame[::-1]
            # print(frame)
            # threshold = 0.79
            # draw(self.frame, self.template1, threshold)
            # draw(self.frame, self.template2, threshold)
            # draw(self.frame, self.template3, threshold)
            # draw(self.frame, self.template4, threshold)
            # draw(self.frame, self.template5, threshold)
            # draw(self.frame, self.template6, threshold)
            # draw(self.frame, self.template7, threshold)
            with HiddenPrints():
                self.frame = self.predictor.detect(self.frame)
            #self.frame = self.predictor.draw_boxes(self.frame, all_box, prob)

            #cv2.rectangle(self.frame, (50, 100), (100, 200), (0, 255, 0), 6)
            self.signal.emit()
            sleep(0.01)
