from enum import Enum
from time import sleep

import cv2
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QMutex, Qt, QThread, Signal

from det.nanodet import NanoDet
from tello import FrameThread


class DetectMethod(Enum):
    NANODET = 0
    YOLOV5 = 1
    TEMPLATE_MATCHING = 2


class DetectThread(QThread):
    signal = Signal()
    mutex = QMutex()

    def __init__(self, frameThread: FrameThread):
        super(DetectThread, self).__init__()

        self.frameThread = frameThread
        self.frame = None
        self.detect_realtime = True
        self.detect_method = DetectMethod.NANODET
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

            if self.detect_realtime:
                if self.detect_method == DetectMethod.NANODET:
                    # with HiddenPrints():
                    self.frame = self.predictor.detect(self.frame)
                elif self.detect_method == DetectMethod.NANODET:
                    pass
                elif self.detect_method == DetectMethod.NANODET:
                    pass

            else:
                pass

            #self.frame = self.predictor.draw_boxes(self.frame, all_box, prob)

            #cv2.rectangle(self.frame, (50, 100), (100, 200), (0, 255, 0), 6)
            self.signal.emit()
            sleep(0.01)
