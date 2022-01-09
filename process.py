import os
from enum import IntEnum
import time
from time import sleep

import cv2
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QDateTime, QMutex, Qt, QThread, Signal, Slot
from cv2 import imwrite

from cls.resnet import ResNet
from control import FrameThread, ControlThread
from det.nanodet import NanoDet
from det.nanodet_plus import NanoDetPlus
from det.template import TemplateMatcher
from det.yolov5 import YOLOv5
from simple_pid import PID
from tracker import Tracker
from djitellopy import Tello


class DetMethod(IntEnum):
    NANODET = 0
    YOLOV5 = 1
    TEMPLATE_MATCHING = 2


class ClsMethod(IntEnum):
    RESNET18 = 0
    YOLOV5 = 1


class XModel(object):
    def __init__(self, distance):
        self.distance = distance
        self.scale = 0.37

    def update(self, x_move, dt):
        if x_move >= 0:
            self.distance -= self.scale * x_move * dt
        else:
            self.distance += self.scale * x_move * dt
        return self.distance


class YModel(object):
    def __init__(self, distance):
        self.distance = distance
        self.scale = 0.37

    def update(self, y_move, dt):
        if y_move >= 0:
            self.distance -= self.scale * y_move * dt
        else:
            self.distance += self.scale * y_move * dt
        return self.distance


class ProcessThread(QThread):
    signal = Signal()
    mutex = QMutex()

    def __init__(self, tello: Tello, frameThread: FrameThread, controlThread: ControlThread):
        super(ProcessThread, self).__init__()

        self.frameThread = frameThread
        self.controlThread = controlThread
        self.frame = None

        # detection
        self.conf = 0.4
        self.det_realtime = True
        self.det_method = DetMethod.NANODET
        self.classes = ["storage-tank", "mine", "ship", "field", "plane"]
        self.nanodet = NanoDetPlus(
            './det/model/nanodet_uav.onnx', self.classes)
        self.yolo = YOLOv5('./det/model/yolov5n_uav.onnx')

        # template
        template_dir = './det/model/template/'
        template_path = [template_dir +
                         path for path in os.listdir(template_dir)]
        templates = [cv2.imread(path) for path in template_path]
        self.template_matcher = TemplateMatcher(templates)

        # cls
        self.cls_realtime = True
        self.cls_result = ''
        self.cls_method = ClsMethod.RESNET18
        self.classifier = ResNet()

        # Track
        self.tello = tello
        self.enable_tracking = False
        self.start_tracking = False
        self.tracker = Tracker()
        # self.pid

    def run(self):
        # i = 0
        # minsize = 7000
        # model = NanoDetPlus('./det/model/nanodet_car.onnx')
        #start_time = time.time()
        #last_time = start_time
        # x_model = XModel(self.x_distance)
        # y_model = YModel(self.y_distance)
        # x_pid = PID(0.001, 0.1, 0.05, setpoint=1)
        # y_pid = PID(0.001, 0.05, 0.01, setpoint=1)
        while True:
            self.mutex.lock()
            self.frame = self.frameThread.img
            self.mutex.unlock()

            if self.frame is None:
                continue

            # classification
            if self.cls_realtime:
                self.cls_result = self.classifier.infer(self.frame)

            # detection
            if self.det_realtime:
                if self.det_method == DetMethod.NANODET:
                    self.frame = self.nanodet.detect(self.frame)
                elif self.det_method == DetMethod.YOLOV5:
                    self.frame = self.yolo.detect(self.frame)
                elif self.det_method == DetMethod.TEMPLATE_MATCHING:
                    self.frame = self.template_matcher.detect(self.frame)

            # tracking
            if self.enable_tracking:
                self.frame, success_flag, x, y = self.tracker.update(
                    self.frame)
                if self.start_tracking:
                    if success_flag:
                        y = self.frame.shape[0]-y
                        dx = x-self.frame.shape[1]/2
                        dy = y-self.frame.shape[0]/2
                        print(dx, dy)
                        self.tello.send_rc_control(
                            int(dx*0.07), int(dy*0.07), 0, 0)
            # else:
            #     pass
            #self.frame = frame
            self.signal.emit()
            sleep(0.01)

    def zheshishenme(self):
        if self.enable_tracking:
            while not self.end_tracking:
                if self.init_rect is not None:
                    # TODO bbox(x,y,w,h)
                    # x, y, w, h = tuple(np.array(self.init_rect).astype(np.int64))
                    x, y, w, h = 0
                    self.x_distance = x + w / 2 - self.frame.shape[1] / 2
                    self.y_distance = y + h / 2 - self.frame.shape[0] / 2
                    x_model = XModel(self.x_distance)
                    y_model = YModel(self.y_distance)
                    x_pid = PID(0.00001, 0.001, 0.0005, setpoint=1)
                    y_pid = PID(0.00001, 0.0005, 0.0001, setpoint=1)
                    start_time = time.time()
                    last_time = start_time
                    while not self.end_tracking:
                        current_time = time.time()
                        dt = current_time - last_time
                        last_time = current_time

                        x_move = x_pid(self.x_distance)
                        y_move = y_pid(self.y_distance)
                        self.x_distance = x_model.update(x_move, dt)
                        print('x_distance: ', self.x_distance)
                        self.y_distance = y_model.update(y_move, dt)
                        print('y_distance: ', self.y_distance)
                        self.controlThread.x_move = x_move
                        self.controlThread.y_move = y_move

                        # if x_move <= 0:
                        #     self.drone.send_command('right' + ' ' + str(-x_move))
                        # else:
                        #     self.drone.send_command('left' + ' ' + str(x_move))
                        # if y_move >= 0:
                        #     self.drone.send_command('back' + ' ' + str(y_move))
                        # else:
                        #     self.drone.send_command('forward' + ' ' + str(-y_move))

                        if self.x_distance <= 4 and self.y_distance <= 4:
                            break
                        if self.end_tracking:
                            break

    @Slot()
    def set_det_realtime(self, checked: bool):
        self.det_realtime = checked
        if checked:
            print('启用目标检测')
        else:
            print('禁用目标检测')

    @Slot()
    def set_cls_realtime(self, checked: bool):
        self.cls_realtime = checked
        if checked:
            print('启用场景分类')
        else:
            print('禁用场景分类')

    @Slot()
    def set_det_method(self, i: int):
        self.det_method = i
        # self.det_method=DetMethod.NAN
        print('当前检测算法为: '+str(self.det_method))

    def set_conf_th(self, conf):
        self.nanodet.prob_threshold = conf
        self.yolo.prob_threshold = conf

    @Slot(bool)
    def set_tracking_state(self, checked: bool):
        self.start_tracking = checked
        if checked:
            print('开始追踪目标')
        else:
            print('停止追踪目标')


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

    @Slot()
    def start_record(self):
        self.is_recording = True

    @Slot()
    def stop_record(self):
        self.is_recording = False
