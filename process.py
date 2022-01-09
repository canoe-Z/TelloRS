import os
from enum import Enum
import time
from time import sleep

import cv2
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QDateTime, QMutex, Qt, QThread, Signal

from cls.resnet import ResNet
from control import FrameThread, ControlThread
from det.nanodet import NanoDet
from det.nanodet_plus import NanoDetPlus
from det.template import TemplateMatcher
from det.yolov5 import YOLOv5
from simple_pid import PID


class DetMethod(Enum):
    NANODET = 0
    YOLOV5 = 1
    TEMPLATE_MATCHING = 2


class ClsMethod(Enum):
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

    def __init__(self, frameThread: FrameThread, controlThread: ControlThread):
        super(ProcessThread, self).__init__()

        self.conf = 0.4

        self.frameThread = frameThread
        self.controlThread = controlThread
        self.frame = None

        # nanodet
        self.det_realtime = True
        self.det_method = DetMethod.NANODET
        #self.detector = NanoDet()

        # YOLOV5
        #self.detector = YOLOv5()

        self.detector = NanoDetPlus('./det/model/nanodet_uav.onnx')
        # template
        template_dir = './det/model/template'
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
        self.enable_tracking = False
        self.end_tracking = False
        self.start_tracking = False
        self.tracker = cv2.TrackerCSRT_create()

        self.track_flag = 0

    def run(self):
        i = 0
        minsize = 7000
        model = NanoDetPlus('./det/model/nanodet_car.onnx')
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
            # if self.frame is None:
            #     continue
            # else:
            #     i += 1

            # #frame = self.frame.copy()
            # if i == 1:
            #     box = model.detect2(self.frame)
            #     if(len(box) == 0):
            #         i = 0
            #         cv2.putText(self.frame, "Tracking failure detected", (100, 80),
            #                     cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            #         self.signal.emit()
            #         sleep(0.01)
            #         continue
            #     ok = self.tracker.init(self.frame, box)
            #     if not ok:
            #         self.signal.emit()
            #         sleep(0.01)
            #         continue
            # success, bbox = self.tracker.update(self.frame)

            # centerx = int(bbox[0]+(bbox[2])/2)
            # centery = int(bbox[1]+(bbox[3])/2)
            # if(self.frame[centery, centerx, 0] <= 150 and self.frame[centery, centerx, 1] <= 150 and self.frame[centery, centerx, 2] <= 150):
            #     success = 0

            # if success:
            #     p1 = (int(bbox[0]), int(bbox[1]))
            #     p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            #     cv2.rectangle(self.frame, p1, p2, (255, 0, 0), 2, 1)
            # else:
            #     i = 0
            # # if(box[2]*box[3] < minsize):
            # #     print("框较小")
            # #     i = 0

            # x_distance = centerx - self.frame.shape[1] / 2
            # y_distance = centery - self.frame.shape[0] / 2


            # x_model = XModel(x_distance)
            # y_model = YModel(y_distance)
            # x_pid = PID(0.0001, 0.01, 0.005, setpoint=1)
            # y_pid = PID(0.0001, 0.005, 0.001, setpoint=1)
            # start_time = time.time()
            # last_time = start_time
            # while True:
            #     current_time = time.time()
            #     dt = current_time - last_time
            #     last_time = current_time

            #     x_move = x_pid(x_distance)
            #     y_move = y_pid(y_distance)
            #     x_distance = x_model.update(x_move, dt)
            #     #print('x_distance: ', self.x_distance)
            #     y_distance = y_model.update(y_move, dt)
            #     print(x_move, y_move, x_distance, y_distance)
            #     #print('y_distance: ', self.y_distance)
            #     if x_distance <= 4 and y_distance <= 4:
            #         break
            # break

            # cls
            # if self.cls_realtime:
            #     self.cls_result = self.classifier.test(self.frame)
            #     # print(result)

            # # det
            # if self.det_realtime:
            #     if self.det_method == DetMethod.NANODET:
            #         self.detector.prob_threshold = self.conf
            #         self.frame = self.detector.detect(self.frame)
            #     elif self.det_method == DetMethod.YOLOV5:
            #         pass
            #     elif self.det_method == DetMethod.TEMPLATE_MATCHING:
            #         self.frame = self.template_matcher.detect(self.frame)

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
