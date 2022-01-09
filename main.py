import os
import queue
import sys

import cv2
from djitellopy import Tello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QDateTime, Qt, QThread, Signal, Slot
from PySide6.QtWidgets import QMainWindow

from control import ControlMode, ControlThread, FrameThread
from nav import IMUThread, MatchingThread, autoThread, PointThread
from process import ProcessThread, VideoWriter
from ui.ClickJumpSlider import ClickJumpSlider
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
        #self.move_distance = 30

        self.ui.action_connect.triggered.connect(self.connect_tello)
        self.ui.action_takephoto.triggered.connect(self.take_photo)

        self.ui.listWidget.currentRowChanged.connect(
            self.ui.stackedWidget.setCurrentIndex)

        self.control_mode = ControlMode.FIXED_MODE
        self.ui.rbtn_move_fixed.setChecked(True)
        # self.ui.rbtn_move_fixed_3.setChecked(True)
        self.ui.rbtn_move_single.clicked.connect(
            lambda: self.set_control_mode(ControlMode.SINGLE_MODE))
        self.ui.rbtn_move_rc.clicked.connect(
            lambda: self.set_control_mode(ControlMode.RC_MODE))
        self.ui.rbtn_move_fixed.clicked.connect(
            lambda: self.set_control_mode(ControlMode.FIXED_MODE))
        # 第三页的控制模块
        self.ui.rbtn_move_single_3.clicked.connect(
            lambda: self.set_control_mode(ControlMode.SINGLE_MODE))
        self.ui.rbtn_move_rc_3.clicked.connect(
            lambda: self.set_control_mode(ControlMode.RC_MODE))
        self.ui.rbtn_move_fixed_3.clicked.connect(
            lambda: self.set_control_mode(ControlMode.FIXED_MODE))

        # self.ui.chk_autocap.stateChanged.connect(self.chk_autocap)

        # 滑动条连接
        self.ui.slider_step_1.setValue(30)
        self.ui.slider_step_3.setValue(30)
        self.ui.slider_speed_1.setValue(self.rc_speed)
        self.ui.slider_speed_3.setValue(self.rc_speed)
        self.ui.slider_step_1.setMinimum(20)  # 最小值
        self.ui.slider_step_1.setMaximum(100)  # 最大值
        self.ui.slider_step_1.valueChanged.connect(self.movestep_1)
        self.ui.slider_step_3.setMinimum(20)  # 最小值
        self.ui.slider_step_3.setMaximum(100)  # 最大值
        self.ui.slider_step_3.valueChanged.connect(self.movestep_3)

        self.ui.slider_speed_1.setMinimum(10)  # 最小值
        self.ui.slider_speed_1.setMaximum(50)  # 最大值
        self.ui.slider_speed_1.valueChanged.connect(self.movespeed_1)
        self.ui.slider_speed_3.setMinimum(10)  # 最小值
        self.ui.slider_speed_3.setMaximum(50)  # 最大值
        self.ui.slider_speed_3.valueChanged.connect(self.movespeed_3)

        self.ui.slider_conf.setMinimum(1)
        self.ui.slider_conf.setMaximum(100)
        self.ui.slider_conf.valueChanged.connect(self.change_conf)
        self.ui.slider_conf.setValue(40)

        self.ui.autotargetbutton.clicked.connect(self.autoThread1)  # 自动巡检

        self.ui.action_record.triggered.connect(self.start_record)
        self.ui.action_stoprecord.triggered.connect(self.stop_record)

        self.ui.loadpic_4.clicked.connect(self.openpic)

        # self.ui.pushButton.clicked.connect(self.start_record)
        # self.ui.pushButton_2.clicked.connect(self.stop_record)
        # self.ui.pushButton_3.clicked.connect(self.auto)self.start_record

        # self.ui.gb_det.clicked.connect(self.print_state)

        # self.ui.loadpic_4.clicked.connect(self.loadpicture)
        # self.ui.savepic_4.clicked.connect(self.savepicture)

    # 第二页自动巡检开启

    def autoThread1(self):
        # autoThread.start()
        #self.point_thread.set_init_pos(0, 0)
        self.point_thread.set_end_pos(500, 500)
        self.point_thread.start()

    # 滑动条触发控制

    def movestep_1(self):
        self.ui.label_step_1.setText(
            str('步长：'+str(self.ui.slider_step_1.value())))
        self.ui.slider_step_3.setValue(self.ui.slider_step_1.value())
        self.control_thread.move_distance = self.ui.slider_step_1.value()

    def movestep_3(self):
        self.ui.label_step_3.setText(
            str('步长：'+str(self.ui.slider_step_3.value())))
        self.ui.slider_step_1.setValue(self.ui.slider_step_3.value())
        self.control_thread.move_distance = self.ui.slider_step_3.value()

    def movespeed_1(self):
        self.ui.label_speed_1.setText(
            str('转速：'+str(self.ui.slider_speed_1.value())))
        self.ui.slider_speed_3.setValue(self.ui.slider_speed_1.value())
        self.rc_speed = self.ui.slider_speed_1.value()

    def movespeed_3(self):
        self.ui.label_speed_3.setText(
            str('转速：'+str(self.ui.slider_speed_3.value())))
        self.ui.slider_speed_1.setValue(self.ui.slider_speed_3.value())
        self.rc_speed = self.ui.slider_speed_3.value()

    def change_conf(self):
        self.ui.label_conf.setText(
            str('阈值：'+str(self.ui.slider_conf.value()/100)))
        self.process_thread.conf = self.ui.slider_conf.value()/100

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
        qImg2 = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template_2.width(), self.ui.label_template_2.height())
        qImg3 = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template_3.width(), self.ui.label_template_3.height())
        self.ui.label_template.setPixmap(qImg)
        self.ui.label_template_2.setPixmap(qImg2)
        self.ui.label_template_3.setPixmap(qImg3)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if not self.tello_connected:
            return

        key = event.key()

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
        self.point_thread = PointThread(self.tello, auto_queue)

        # self.frame_thread.signal.connect(self.show_tello_frame)
        self.frame_thread.start()

        self.video_writer = VideoWriter(self.frame_thread)
        self.video_writer.start()

        self.process_thread = ProcessThread(
            self.frame_thread, self.control_thread)
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
        qImg2 = QtGui.QPixmap(qImg).scaled(
            self.ui.label_map_2.width(), self.ui.label_map_2.height())
        self.ui.label_source.setPixmap(qImg)
        self.ui.label_map_2.setPixmap(qImg2)

        # 尝试获取坐标
        self.ui.label_map_2.mousePressEvent = self.getPos

    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print(x, y)

    @Slot()
    def show_det(self):
        qImg = cv2toQImage(self.process_thread.frame)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template.width(), self.ui.label_template.height())
        qImg2 = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template_2.width(), self.ui.label_template_2.height())
        qImg3 = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template_3.width(), self.ui.label_template_3.height())
        self.ui.label_template.setPixmap(qImg)
        self.ui.label_template_2.setPixmap(qImg2)
        self.ui.label_template_3.setPixmap(qImg3)
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

    @Slot()
    def openpic(self, Filepath):
        directory = QtWidgets.QFileDialog.getOpenFileName(
            self, "选取图片文件", "./", "All Files (*);;jpg文件 (*.jpg);;png文件 (*.png);;bmp文件 (*.bmp)")
        qImg = cv2toQImage(cv2.imread(directory[0]))
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_pic4.width(), self.ui.label_pic4.height())
        self.ui.label_pic4.setPixmap(qImg)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()

    sys.exit(app.exec())
