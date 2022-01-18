import os
import time
from collections import deque
from enum import IntEnum

import cv2
from djitellopy import Tello
from PySide6.QtCore import QDateTime, QMutex, QThread, Signal, Slot
from simple_pid import PID

from cls.classfier import Classfier
from control import ControlThread, FrameThread
from det.nanodet_plus import NanoDetPlus
from det.template import TemplateMatcher
from det.utils.yolov5_utils import letterbox
from det.yolov5 import YOLOv5
from nav import IMUThread
from tracker import Tracker


class DetMethod(IntEnum):
    NANODET = 0
    YOLOV5 = 1
    TEMPLATE_MATCHING = 2


class ClsMethod(IntEnum):
    RESNET = 0
    SHUFFLENET = 1
    MOBILENET = 2


class ProcessThread(QThread):
    signal = Signal()
    recent_signal = Signal()
    mutex = QMutex()

    def __init__(self, tello: Tello, frame_thread: FrameThread, control_thread: ControlThread, IMU_thread: IMUThread):
        super(ProcessThread, self).__init__()

        self.frame_thread = frame_thread
        self.control_thread = control_thread
        self.IMU_thread = IMU_thread
        self.frame = None

        # detection
        self.conf = 0.4
        self.det_realtime = True
        self.show_recent_dets = False
        self.recent_dets = deque()
        self.det_method = DetMethod.NANODET
        self.classes = ["storage-tank", "mine", "ship", "field", "plane"]
        self.classes_cn = ["油罐", "矿井", "舰船", "农田", "飞机"]
        self.nanodet = NanoDetPlus(
            './det/model/nanodet_uav.onnx', self.classes)
        self.yolo = YOLOv5('./det/model/yolov5n_uav.onnx', self.classes)

        # template
        template_dir = './det/model/template/'
        template_path = [template_dir +
                         path for path in os.listdir(template_dir)]
        templates = [cv2.imread(path) for path in template_path]
        self.template_matcher = TemplateMatcher(templates)

        # cls
        self.cls_realtime = True
        self.cls_result = ''
        self.cls_method = ClsMethod.RESNET
        self.resnet = Classfier('./cls/model/resnet18.onnx')
        self.shufflenet = Classfier('./cls/model/shufflenet_v2_x1_0.onnx')
        self.mobilenet = Classfier('./cls/model/mobilenet_v3_small.onnx')

        # Track
        self.tello = tello
        self.enable_tracking = False
        self.start_tracking = False
        self.tracker = Tracker()

        # PID
        self.pid_x = PID(0.085, 0.01, 0.01, setpoint=0)
        self.pid_y = PID(0.085, 0.01, 0.01, setpoint=0)
        self.pid_x.output_limits = (-30, 30)
        self.pid_y.output_limits = (-30, 30)

    def run(self):
        frame_num = 0
        while True:
            self.mutex.lock()
            self.frame = self.frame_thread.img
            self.mutex.unlock()

            if self.frame is None:
                continue

            # classification
            if self.cls_realtime:
                if self.cls_method == ClsMethod.RESNET:
                    self.cls_result = self.resnet.infer(self.frame)
                elif self.cls_method == ClsMethod.SHUFFLENET:
                    self.cls_result = self.shufflenet.infer(self.frame)
                elif self.cls_method == ClsMethod.MOBILENET:
                    self.cls_result = self.mobilenet.infer(self.frame)

            # detection
            if self.det_realtime:
                if self.det_method == DetMethod.NANODET:
                    dets = self.nanodet.detect(self.frame)
                elif self.det_method == DetMethod.YOLOV5:
                    dets = self.yolo.detect(self.frame)
                elif self.det_method == DetMethod.TEMPLATE_MATCHING:
                    dets = self.template_matcher.detect(self.frame)

                if self.show_recent_dets:
                    if frame_num % 20 == 0:
                        for i in range(min(len(dets), 3)):
                            xmin, ymin, xmax, ymax, classid, _ = dets[i]

                            # 求相对位移
                            x = (xmin+xmax)/2
                            y = (ymin+ymax)/2
                            y = self.frame.shape[0]-y
                            dx = x-self.frame.shape[1]/2
                            dy = y-self.frame.shape[0]/2

                            # tello坐标,平面坐标系
                            tello_x = -self.IMU_thread.pos[1]
                            tello_y = self.IMU_thread.pos[0]

                            # 目标真实坐标
                            x = int(dx*0.1 + tello_x)
                            y = int(dy*0.1 + tello_y)

                            bbox_img = None
                            try:
                                bbox_img, _, _ = letterbox(
                                    self.frame[ymin:ymax, xmin:xmax], (117, 95), (0, 0, 0), False, False)
                            except:
                                pass

                            if bbox_img is not None:
                                self.recent_dets.append(
                                    (bbox_img, self.classes_cn[classid], (x, y)))

                        while len(self.recent_dets) > 3:
                            self.recent_dets.popleft()

                        self.recent_signal.emit()
                        frame_num = 0

                self.frame = self.draw_bbox(self.frame, dets)

            # tracking
            if self.enable_tracking:
                self.frame, success_flag, x, y = self.tracker.update(
                    self.frame)
                if self.start_tracking:
                    if success_flag:
                        y = self.frame.shape[0]-y
                        dx = self.frame.shape[1]/2-x
                        dy = self.frame.shape[0]/2-y

                        vx = int(self.pid_x(dx))
                        vy = int(self.pid_y(dy))
                        print(dx, dy, vx, vy)
                        self.tello.send_rc_control(vx, vy, 0, 0)

            frame_num += 1
            self.signal.emit()
            time.sleep(0.01)

    def draw_bbox(self, frame, dets):
        for det in dets:
            xmin, ymin, xmax, ymax, class_id, conf = det
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax),
                          (0, 0, 255), thickness=3)
            cv2.putText(frame, self.classes[class_id] + ': ' + str(round(conf, 3)), (xmin, ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), thickness=1)
        return frame

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
        print('当前检测算法为: '+str(self.det_method))

    @Slot()
    def set_cls_method(self, i: int):
        self.cls_method = i
        print('当前分类算法为: '+str(self.cls_method))

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
                    time.sleep(1 / self.fps)
            time.sleep(0.01)

    @Slot()
    def start_record(self):
        self.is_recording = True

    @Slot()
    def stop_record(self):
        self.is_recording = False
