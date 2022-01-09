import queue
import sys

import cv2
from djitellopy import Tello
from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import QDateTime, Qt, Slot
from PySide6.QtWidgets import QMainWindow, QLabel

from control import ControlMode, ControlThread, FrameThread
from nav import IMUThread, MatchingThread, AutoFlightThread, PointFlightThread
from process import ProcessThread, VideoWriter
from ui.MainWindow import Ui_MainWindow
from utils.control import lut_key, send_rc_control_by_key
from utils.img import cv2toQImage


class TelloRS(QMainWindow):
    def __init__(self):
        super(TelloRS, self).__init__()

        self.tello_connected = False
        self.rc_speed = 30
        self.is_autocap = False
        self.is_shownav = True

        # init tello and threads
        self.tello = Tello()
        self.map = cv2.imread('./match/map.png')
        self.map_dst = self.map.copy()

        nav_queue = queue.Queue()
        nav_queue.maxsize = 1
        auto_queue = queue.Queue()
        auto_queue.maxsize = 1

        self.frame_thread = FrameThread(self.tello)
        self.matching_thread = MatchingThread(
            self.frame_thread, self.map, nav_queue)
        self.control_thread = ControlThread(self.tello)
        self.imu_thread = IMUThread(self.tello, nav_queue, auto_queue)
        self.video_writer = VideoWriter(self.frame_thread)
        self.process_thread = ProcessThread(self.tello,
                                            self.frame_thread, self.control_thread)
        self.auto_thread = AutoFlightThread(
            self.tello, auto_queue, self.frame_thread)
        self.point_thread = PointFlightThread(self.tello, auto_queue)

        # signal
        self.frame_thread.signal.connect(self.show_battery)
        self.control_thread.finish_signal.connect(self.command_finish)
        self.imu_thread.sift_signal.connect(self.draw_sift_pos)
        self.imu_thread.imu_signal.connect(self.draw_imu_pos)
        self.process_thread.signal.connect(self.show_det)
        # self.matching_thread.finish_signal.connect(self.show_map)

        # init ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFocus()
        self.set_map(self.map)

        # sidebar
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.listWidget.currentRowChanged.connect(
            self.set_page)

        # toolbar
        self.ui.action_connect.triggered.connect(self.connect_tello)
        self.ui.action_takephoto.triggered.connect(self.take_photo)
        self.ui.action_record.triggered.connect(self.video_writer.start_record)
        self.ui.action_stoprecord.triggered.connect(
            self.video_writer.stop_record)

        # statusbar
        self.label_battery = QLabel('')
        self.ui.statusbar.addPermanentWidget(self.label_battery, stretch=0)

        # page 1
        self.control_mode = ControlMode.FIXED_MODE
        self.ui.rbtn_move_fixed.setChecked(True)
        self.ui.rbtn_move_single.clicked.connect(
            lambda: self.set_control_mode(ControlMode.SINGLE_MODE))
        self.ui.rbtn_move_single.clicked.connect(
            lambda: self.ui.rbtn_move_single_3.setChecked(True))

        self.ui.rbtn_move_rc.clicked.connect(
            lambda: self.set_control_mode(ControlMode.RC_MODE))
        self.ui.rbtn_move_rc.clicked.connect(
            lambda: self.ui.rbtn_move_rc_3.setChecked(True))

        self.ui.rbtn_move_fixed.clicked.connect(
            lambda: self.set_control_mode(ControlMode.FIXED_MODE))
        self.ui.rbtn_move_fixed.clicked.connect(
            lambda: self.ui.rbtn_move_fixed_3.setChecked(True))
        self.ui.gb_det.toggled.connect(self.process_thread.set_det_realtime)
        self.ui.gb_cls.toggled.connect(self.process_thread.set_cls_realtime)
        self.ui.cb_det.currentIndexChanged.connect(
            self.process_thread.set_det_method)
        self.ui.slider_step_1.setValue(30)
        self.ui.slider_speed_1.setValue(self.rc_speed)
        self.ui.slider_step_1.setMinimum(20)
        self.ui.slider_step_1.setMaximum(100)
        self.ui.slider_step_1.valueChanged.connect(self.change_movestep_p1)
        self.ui.slider_speed_1.setMinimum(10)
        self.ui.slider_speed_1.setMaximum(50)
        self.ui.slider_speed_1.valueChanged.connect(self.change_movespeed_p1)
        self.ui.slider_conf.setMinimum(1)
        self.ui.slider_conf.setMaximum(100)
        self.ui.slider_conf.valueChanged.connect(self.change_det_conf)
        self.ui.slider_conf.setValue(35)

        self.ui.btn_clean_nav.clicked.connect(self.reset_map)
        self.ui.cb_show_nav.clicked.connect(self.set_autocap)
        self.ui.cb_autocap.clicked.connect(self.set_shownav)

        # page 2
        self.ui.btn_autoflight.clicked.connect(self.start_auto_flight)
        self.ui.btn_pointflight.clicked.connect(self.start_point_flight)
        self.ui.label_map_2.mousePressEvent = self.get_map_pos  # 尝试获取坐标

        # page 3
        self.ui.rbtn_move_fixed_3.setChecked(True)
        self.ui.rbtn_move_single_3.clicked.connect(
            lambda: self.set_control_mode(ControlMode.SINGLE_MODE))
        self.ui.rbtn_move_single_3.clicked.connect(
            lambda: self.ui.rbtn_move_single.setChecked(True))
        self.ui.rbtn_move_rc_3.clicked.connect(
            lambda: self.set_control_mode(ControlMode.RC_MODE))
        self.ui.rbtn_move_rc_3.clicked.connect(
            lambda: self.ui.rbtn_move_rc.setChecked(True))
        self.ui.rbtn_move_fixed_3.clicked.connect(
            lambda: self.set_control_mode(ControlMode.FIXED_MODE))
        self.ui.rbtn_move_fixed_3.clicked.connect(
            lambda: self.ui.rbtn_move_fixed.setChecked(True))
        self.ui.slider_step_3.setValue(30)
        self.ui.slider_speed_3.setValue(self.rc_speed)
        self.ui.slider_step_3.setMinimum(20)  # 最小值
        self.ui.slider_step_3.setMaximum(100)  # 最大值
        self.ui.slider_step_3.valueChanged.connect(self.change_movestep_p3)
        self.ui.slider_speed_3.setMinimum(10)  # 最小值
        self.ui.slider_speed_3.setMaximum(50)  # 最大值
        self.ui.slider_speed_3.valueChanged.connect(self.change_movespeed_p3)
        self.ui.cb_tracking.toggled.connect(
            self.process_thread.set_tracking_state)

        # page 4
        self.ui.loadpic_4.clicked.connect(self.openpic)
        self.ui.savepic_4.clicked.connect(self.savepic)

    def set_map(self, map):
        qImg = cv2toQImage(map)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_source.width(), self.ui.label_source.height())
        qImg2 = QtGui.QPixmap(qImg).scaled(
            self.ui.label_map_2.width(), self.ui.label_map_2.height())
        self.ui.label_source.setPixmap(qImg)
        self.ui.label_map_2.setPixmap(qImg2)

    def get_map_pos(self, event):
        self.map_x = int(event.position().x()*1280/400)
        self.map_y = int((400-event.position().y())*1280/400)

        self.ui.label_pos_2.setText(
            str('坐标: ('+str(self.map_x)+','+str(self.map_y))+')')

    @Slot()
    def set_page(self, page: int):
        if self.ui.stackedWidget.currentIndex() == 0:
            self.last_cls_state = self.process_thread.cls_realtime
            self.last_det_state = self.process_thread.det_realtime

        self.ui.stackedWidget.setCurrentIndex(page)
        if page == 0:
            self.ui.gb_cls.setChecked(self.last_cls_state)
            self.ui.gb_det.setChecked(self.last_det_state)
        elif page == 1:
            self.ui.gb_cls.setChecked(False)
            self.ui.gb_det.setChecked(True)
        else:
            self.ui.gb_cls.setChecked(False)
            self.ui.gb_det.setChecked(False)

        if page == 3:
            self.process_thread.enable_tracking = True
        else:
            self.process_thread.enable_tracking = False
            self.ui.cb_tracking.setChecked(False)

    @Slot()
    def show_battery(self):
        self.label_battery.setText(
            'Tello已连接! 电源剩余: '+str(self.frame_thread.tello_battery))

    # TODO 自动巡检
    @Slot()
    def start_auto_flight(self):
        self.auto_thread.start()

    @Slot()
    def start_point_flight(self):
        self.point_thread.set_end_pos(self.map_x, self.map_y)
        self.point_thread.start()

    @Slot()
    def change_movestep_p1(self):
        self.ui.label_step_1.setText(
            str('步长: '+str(self.ui.slider_step_1.value())))
        self.ui.slider_step_3.setValue(self.ui.slider_step_1.value())
        self.control_thread.move_distance = self.ui.slider_step_1.value()

    @Slot()
    def change_movestep_p3(self):
        self.ui.label_step_3.setText(
            str('步长: '+str(self.ui.slider_step_3.value())))
        self.ui.slider_step_1.setValue(self.ui.slider_step_3.value())
        self.control_thread.move_distance = self.ui.slider_step_3.value()

    @Slot()
    def change_movespeed_p1(self):
        self.ui.label_speed_1.setText(
            str('转速: '+str(self.ui.slider_speed_1.value())))
        self.ui.slider_speed_3.setValue(self.ui.slider_speed_1.value())
        self.rc_speed = self.ui.slider_speed_1.value()

    @Slot()
    def change_movespeed_p3(self):
        self.ui.label_speed_3.setText(
            str('转速: '+str(self.ui.slider_speed_3.value())))
        self.ui.slider_speed_1.setValue(self.ui.slider_speed_3.value())
        self.rc_speed = self.ui.slider_speed_3.value()

    @Slot()
    def change_det_conf(self):
        conf_th = self.ui.slider_conf.value()/100
        self.ui.label_conf.setText(
            str('阈值: '+str(conf_th)))
        self.process_thread.set_conf_th(conf_th)

    @Slot(bool)
    def set_autocap(self, checked: bool):
        self.is_autocap = checked

    @Slot(bool)
    def set_shownav(self, checked: bool):
        self.is_shownav = checked

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

    @Slot()
    def connect_tello(self):
        self.ui.statusbar.showMessage('正在连接Tello...')
        self.frame_thread.connect_tello()

        self.frame_thread.start()
        self.video_writer.start()
        self.process_thread.start()
        self.matching_thread.start()
        self.control_thread.start()
        self.imu_thread.start()

        self.ui.statusbar.showMessage('连接成功!')
        self.tello_connected = True

    @Slot()
    def draw_sift_pos(self):
        if self.is_shownav:
            self.map_dst = cv2.circle(self.map_dst, (int(self.matching_thread.cx), int(
                self.matching_thread.cy)), 4, (0, 0, 255), 10)
            self.set_map(self.map_dst)

    @Slot()
    def draw_imu_pos(self):
        if self.is_shownav:
            self.map_dst = cv2.circle(self.map_dst, (-int(self.imu_thread.pos[1]), 1280-int(self.imu_thread.pos[0])),
                                      4, (0, 255, 0), 10)
            self.set_map(self.map_dst)

    @Slot()
    def reset_map(self):
        self.map_dst = self.map.copy()
        self.set_map(self.map_dst)

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
        # if self.is_autocap:
        #     cv2.imwrite('./output/'+curDataTime+'.png', self.frame_thread.img)

    @Slot()
    def openpic(self):
        directory = QtWidgets.QFileDialog.getOpenFileName(
            self, "选取图片文件", "./", "All Files (*);;jpg文件 (*.jpg);;png文件 (*.png);;bmp文件 (*.bmp)")
        self.pic_4 = cv2.imread(directory[0])
        qImg = cv2toQImage(self.pic_4)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_pic4.width(), self.ui.label_pic4.height())
        self.ui.label_pic4.setPixmap(qImg)

    @Slot()
    def savepic(self):
        directory = QtWidgets.QFileDialog.getSaveFileName(
            self, "选择保存路径", "./", "jpg文件 (*.jpg);;png文件 (*.png);;bmp文件 (*.bmp);;All Files (*)")
        cv2.imwrite(directory[0], self.pic_4)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if not self.tello_connected:
            return

        key = event.key()
        if event.isAutoRepeat():
            # keep running while key pressed
            if self.control_mode == ControlMode.FIXED_MODE:
                self.ui.statusbar.showMessage(lut_key(key)+'...')
                self.control_thread.key = key

            elif self.control_mode == ControlMode.RC_MODE:
                send_rc_control_by_key(self.tello, key, self.rc_speed)

        else:
            # only execute once when key pressed
            if self.control_mode == ControlMode.SINGLE_MODE or self.control_mode == ControlMode.FIXED_MODE:
                self.ui.statusbar.showMessage(lut_key(key)+'...')
                self.control_thread.key = key
            elif self.control_mode == ControlMode.RC_MODE:
                if key == Qt.Key_T or key == Qt.Key_L:
                    self.ui.statusbar.showMessage(lut_key(key)+'...')
                    self.control_thread.key = key
                else:
                    send_rc_control_by_key(self.tello, key, self.rc_speed)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if not self.tello_connected:
            return

        if event.isAutoRepeat():
            # keep running while key pressed
            pass
        else:
            # only execute once when key pressed
            if self.control_mode == ControlMode.RC_MODE:
                key = event.key()
                key_list = [Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D,
                            Qt.Key_E, Qt.Key_Q, Qt.Key_R, Qt.Key_F]
                if key in key_list:
                    self.tello.send_rc_control(0, 0, 0, 0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TelloRS()
    window.show()

    sys.exit(app.exec())
