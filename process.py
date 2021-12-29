from enum import Enum
from time import sleep

import cv2
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QMutex, Qt, QThread, Signal
import os

from det.nanodet import NanoDet
from det.template import TemplateMatcher
from control import FrameThread


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

        template_dir = './det/model/template'
        template_path = [template_dir +
                         path for path in os.listdir(template_dir)]
        templates = [cv2.imread(path) for path in template_path]
        self.template_matcher = TemplateMatcher(templates)

    def run(self):
        while True:
            self.mutex.lock()
            self.frame = self.frameThread.img
            self.mutex.unlock()

            if self.detect_realtime:
                if self.detect_method == DetectMethod.NANODET:
                    self.frame = self.predictor.detect(self.frame)
                elif self.detect_method == DetectMethod.YOLOV5:
                    pass
                elif self.detect_method == DetectMethod.TEMPLATE_MATCHING:
                    self.frame = self.template_matcher.detect(self.frame)

            else:
                pass

            #self.frame = self.predictor.draw_boxes(self.frame, all_box, prob)
            #cv2.rectangle(self.frame, (50, 100), (100, 200), (0, 255, 0), 6)
            self.signal.emit()
            sleep(0.01)


class VideoWriter(QThread):
    def __init__(self, frameThread=None):
        super(VideoWriter, self).__init__()
        self.frameThread = frameThread
        self.is_recording = False
        self.video_count = 0
        self.fps = 30
        # self.

    def run(self):
        while True:
            # 保存录像
            if self.is_recording:
                print("正在保存录像...")
                # self.ui.lineEdit_tips.setText("正在保存录像...")
                #self.video_count += 1

                # self.video_width = self.frameThread.img.shape[0]
                # self.video_height = self.frameThread.img.shape[1]

                # fourcc = cv2.VideoWriter_fourcc(*'XVID')
                # video_name = "video" + str(self.video_count) + ".avi"
                # out = cv2.VideoWriter(video_name, fourcc, self.fps, (int(
                #     self.video_width), int(self.video_height)))
                while True:
                    # # 多线程终止条件
                    # if gv.get_value("THREAD_STOP"):
                    #     break
                    # 取当前的实时图像
                    #img = cv2.cvtColor(self.frameThread.img, cv2.COLOR_RGB2BGR)

                    # out.write(img)
                    # 按下停止录像按钮
                    if not self.is_recording:
                        # out.release()
                        print("录像结束")
                        # self.ui.lineEdit_tips.setText(
                        #     "已保存第{}段录像".format(self.video_count))
                        break
                    sleep(1 / self.fps)

            sleep(0.01)
