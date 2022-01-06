import os
import queue
import sys

import cv2
from djitellopy import Tello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QDateTime, Qt, QThread, Signal, Slot
from PySide6.QtWidgets import QMainWindow

from control import ControlMode, ControlThread, FrameThread
from nav import IMUThread, MatchingThread, autoThread
from process import ProcessThread, VideoWriter
from ui.MainWindow import Ui_MainWindow
from utils.control import lut_key
from utils.img import cv2toQImage

# FIX Problem for High DPI and Scale above 100%
# os.environ["QT_FONT_DPI"] = "96"
# os.environ["QT_SCALE_FACTOR"] = "1.5"


class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFocus()

        self.tello_connected = False

        self.cv2_map = cv2.imread('./map/newsource.png')
        self.show_map()

        self.is_autocap = 0

        self.rc_speed = 30
        self.move_distance = 30

        self.ui.action_connect.triggered.connect(self.connect_tello)
        self.ui.action_takephoto.triggered.connect(self.take_photo)

        self.ui.listWidget.currentRowChanged.connect(
            self.ui.stackedWidget.setCurrentIndex)

        self.control_mode = ControlMode.FIXED_MODE
        self.ui.rbtn_move_fixed.setChecked(True)
        self.ui.rbtn_move_single.clicked.connect(
            lambda: self.set_control_mode(ControlMode.SINGLE_MODE))
        self.ui.rbtn_move_rc.clicked.connect(
            lambda: self.set_control_mode(ControlMode.RC_MODE))
        self.ui.rbtn_move_fixed.clicked.connect(
            lambda: self.set_control_mode(ControlMode.FIXED_MODE))

        # self.ui.chk_autocap.stateChanged.connect(self.chk_autocap)

        self.ui.action_record.triggered.connect(self.start_record)
        self.ui.action_stoprecord.triggered.connect(self.stop_record)
        # self.ui.pushButton.clicked.connect(self.start_record)
        # self.ui.pushButton_2.clicked.connect(self.stop_record)
        # self.ui.pushButton_3.clicked.connect(self.auto)

        self.ui.gb_det.clicked.connect(self.print_state)

    def print_state(self, checked: bool):
        self.process_thread.det_realtime = checked

    def start_record(self):
        self.video_writer.is_recording = True

    def stop_record(self):
        self.video_writer.is_recording = False

    @Slot()
    def auto(self):
        self.auto_thread.start()

    @Slot()
    def chk_autocap(self):
        self.is_autocap = self.ui.chk_autocap.isChecked()
        print(self.is_autocap)

    @Slot()
    def show_tello_frame(self):
        qImg = cv2toQImage(self.frame_thread.img)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template.width(), self.ui.label_template.height())
        self.ui.label_template.setPixmap(qImg)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if not self.tello_connected:
            return

        key = event.key()
        print(key)

        if event.isAutoRepeat():
            # 键盘按下反复执行
            if self.control_mode == ControlMode.FIXED_MODE:
                self.ui.statusbar.showMessage(lut_key(key)+'...')
                self.control_thread.key = key

            elif self.control_mode == ControlMode.RC_MODE:
                if key == Qt.Key_W:
                    self.tello.send_rc_control(0, self.rc_speed, 0, 0)
                if key == Qt.Key_A:
                    self.tello.send_rc_control(-self.rc_speed, 0, 0, 0)
                if key == Qt.Key_S:
                    self.tello.send_rc_control(0, -self.rc_speed, 0, 0)
                if key == Qt.Key_D:
                    self.tello.send_rc_control(self.rc_speed, 0, 0, 0)
        else:
            # 按下时执行
            if self.control_mode == ControlMode.SINGLE_MODE or self.control_mode == ControlMode.FIXED_MODE:
                self.ui.statusbar.showMessage(lut_key(key)+'...')
                self.control_thread.key = key
            elif self.control_mode == ControlMode.RC_MODE:
                if key == Qt.Key_T or key == Qt.Key_L:
                    self.ui.statusbar.showMessage(lut_key(key)+'...')
                    self.control_thread.key = key
                else:
                    if key == Qt.Key_W:
                        self.tello.send_rc_control(0, self.rc_speed, 0, 0)
                    if key == Qt.Key_A:
                        self.tello.send_rc_control(-self.rc_speed, 0, 0, 0)
                    if key == Qt.Key_S:
                        self.tello.send_rc_control(0, -self.rc_speed, 0, 0)
                    if key == Qt.Key_D:
                        self.tello.send_rc_control(self.rc_speed, 0, 0, 0)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if not self.tello_connected:
            return

        if event.isAutoRepeat():
            # 键盘按下反复执行
            pass
        else:
            # 按键抬起时执行
            if self.control_mode == ControlMode.RC_MODE:
                key = event.key()
                key_list = [Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D]
                if key in key_list:
                    self.tello.send_rc_control(0, 0, 0, 0)

    @Slot()
    def connect_tello(self):
        self.ui.statusbar.showMessage('正在连接Tello...')

        nav_queue = queue.Queue()
        nav_queue.maxsize = 1
        auto_queue = queue.Queue()
        auto_queue.maxsize = 1
        self.tello = Tello()
        self.frame_thread = FrameThread(self.tello)
        self.matching_thread = MatchingThread(
            self.frame_thread, self.cv2_map, nav_queue)
        self.control_thread = ControlThread(self.tello)
        self.imu_thread = IMUThread(self.tello, nav_queue, auto_queue)
        self.auto_thread = autoThread(
            self.tello, auto_queue, self.frame_thread)

        #self.frame_thread.signal.connect(self.show_tello_frame)
        self.frame_thread.start()

        self.video_writer = VideoWriter(self.frame_thread)
        self.video_writer.start()

        self.process_thread = ProcessThread(self.frame_thread)
        self.process_thread.start()
        self.process_thread.signal.connect(self.show_det)

        self.matching_thread.start()
        self.matching_thread.finish_signal.connect(self.show_map)

        self.control_thread.start()
        self.control_thread.finish_signal.connect(self.command_finish)

        self.imu_thread.start()
        self.imu_thread.sift_signal.connect(self.draw_sift_pos)
        self.imu_thread.imu_signal.connect(self.draw_imu_pos)

        self.ui.statusbar.showMessage('连接成功!')
        self.tello_connected = True

    @Slot()
    def draw_sift_pos(self):
        result = cv2.circle(self.cv2_map, (int(self.matching_thread.cx), int(
            self.matching_thread.cy)), 4, (0, 0, 255), 10)
        qImg = cv2toQImage(result)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_source.width(), self.ui.label_source.height())
        self.ui.label_source.setPixmap(qImg)

    @Slot()
    def draw_imu_pos(self):
        result = cv2.circle(self.cv2_map, (-int(self.imu_thread.pos[1]), 1280-int(self.imu_thread.pos[0])),
                            4, (0, 255, 0), 10)
        qImg = cv2toQImage(result)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_source.width(), self.ui.label_source.height())
        self.ui.label_source.setPixmap(qImg)

    @Slot()
    def show_map(self):
        qImg = cv2toQImage(self.cv2_map)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_source.width(), self.ui.label_source.height())
        self.ui.label_source.setPixmap(qImg)

    @Slot()
    def show_det(self):
        qImg = cv2toQImage(self.process_thread.frame)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template.width(), self.ui.label_template.height())
        self.ui.label_template.setPixmap(qImg)
        self.ui.label_cls_result.setText(self.process_thread.cls_result)

    @Slot()
    def take_photo(self):
        if not self.tello_connected:
            return

        curDataTime = QDateTime.currentDateTime().toString('hh-mm-ss-yyyy-MM-dd')
        cv2.imwrite('output/'+curDataTime+'.png', self.frame_thread.img)
        self.ui.statusbar.showMessage('图像已保存!')

    @Slot(int)
    def set_control_mode(self, mode: int):
        self.control_mode = mode
        print('切换控制模式为'+str(mode))

    @Slot(int)
    def command_finish(self, key: int):
        self.ui.statusbar.showMessage(lut_key(key)+' OK', 2000)
        curDataTime = QDateTime.currentDateTime().toString('hh_mm_ss_yyyy_MM_dd')
        if self.is_autocap:
            cv2.imwrite('./output/'+curDataTime+'.png', self.frame_thread.img)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()

    sys.exit(app.exec())
