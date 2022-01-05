from enum import Enum
from time import sleep

import cv2
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QMutex, Qt, QThread, Signal, QDateTime
import os

from det.nanodet import NanoDet
from det.template import TemplateMatcher
from cls.resnet import ResNet
from control import FrameThread


class DetMethod(Enum):
    NANODET = 0
    YOLOV5 = 1
    TEMPLATE_MATCHING = 2


class ClsMethod(Enum):
    RESNET18 = 0
    YOLOV5 = 1


class ProcessThread(QThread):
    signal = Signal()
    mutex = QMutex()

    def __init__(self, frameThread: FrameThread):
        super(ProcessThread, self).__init__()

        self.frameThread = frameThread
        self.frame = None

        # nanodet
        self.det_realtime = True
        self.det_method = DetMethod.NANODET
        self.detector = NanoDet()

        # template
        template_dir = './det/model/template'
        template_path = [template_dir +
                         path for path in os.listdir(template_dir)]
        templates = [cv2.imread(path) for path in template_path]
        self.template_matcher = TemplateMatcher(templates)

        # cls
        self.cls_realtime = True
        self.cls_method = ClsMethod.RESNET18
        self.classifier = ResNet()

    def run(self):
        while True:
            self.mutex.lock()
            self.frame = self.frameThread.img
            self.mutex.unlock()
            if self.frame is None:
                continue

            # cls
            if self.cls_realtime:
                result = self.classifier.test(self.frame)
                # print(result)

            # det
            if self.det_realtime:
                if self.det_method == DetMethod.NANODET:
                    self.frame = self.detector.detect(self.frame)
                elif self.det_method == DetMethod.YOLOV5:
                    pass
                elif self.det_method == DetMethod.TEMPLATE_MATCHING:
                    self.frame = self.template_matcher.detect(self.frame)

            else:
                pass

            self.signal.emit()
            sleep(0.01)


class VideoWriter(QThread):
    def __init__(self, frameThread: FrameThread):
        super(VideoWriter, self).__init__()
        self.frameThread = frameThread
        self.is_recording = False
        self.video_count = 0
        self.fps = 30

    def run(self):
        while True:
            if self.is_recording:
                print("正在保存录像...")
                self.video_width = self.frameThread.img.shape[0]
                self.video_height = self.frameThread.img.shape[1]
                sz = (int(self.video_height), int(self.video_width))

                curDataTime = QDateTime.currentDateTime().toString('hh-mm-ss-yyyy-MM-dd')
                video_name = "./output/video_" + curDataTime + ".avi"

                fourcc = cv2.VideoWriter_fourcc(*'XVID')

                out = cv2.VideoWriter()
                out.open(video_name, fourcc, self.fps, sz, True)

                while True:
                    out.write(self.frameThread.img)
                    if not self.is_recording:
                        out.release()
                        print("录像结束")
                        break
                    sleep(1 / self.fps)

            sleep(0.01)
