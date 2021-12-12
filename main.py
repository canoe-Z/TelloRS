import queue
import sys

import cv2
from cv2 import imread
from djitellopy import Tello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QMainWindow

from tello import ControlThread, FrameThread
from test_sift import match
from uic.untitled import Ui_MainWindow
from utils.control import lut_key
from utils.img import cv2toQImage


class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_template()
        self.set_source()
        self.template_match()
        self.control_mode = 0

        self.ui.btn_connect.clicked.connect(self.connect_tello)
        self.ui.btn_takephoto.clicked.connect(self.take_photo)
        self.ui.rbtn_move_single.clicked.connect(
            lambda: self.set_control_mode(0))
        self.ui.rbtn_move_rc.clicked.connect(
            lambda: self.set_control_mode(1))

    def count_func(self):
        self.my_thread.start()

    def set_template(self):
        qImg = cv2toQImage(self.my_thread.img)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template.width(), self.ui.label_template.height())  # 设置图片大小
        self.ui.label_template.setPixmap(qImg)  # 设置图片显示

    def set_source(self):
        self.cv2_source = cv2.imread('./data/moban.jpg')
        qImg = cv2toQImage(self.cv2_source)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_source.width(), self.ui.label_source.height())  # 设置图片大小
        self.ui.label_source.setPixmap(qImg)  # 设置图片显示

    def load_template(self):
        self.cv2_template = cv2.imread('./data/target2.jpg')
        qImg = cv2toQImage(self.cv2_template)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_template.width(), self.ui.label_template.height())  # 设置图片大小
        self.ui.label_template.setPixmap(qImg)  # 设置图片显示

    def template_match(self):
        result = match(self.cv2_template, self.cv2_source)
        qImg = cv2toQImage(result)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.ui.label_source.width(), self.ui.label_source.height())  # 设置图片大小
        self.ui.label_source.setPixmap(qImg)  # 设置图片显示

    # 重新实现各事件处理程序
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.isAutoRepeat():
            pass
        else:
            key = event.key()
            if self.control_mode == 0:
                if key == Qt.Key_T or key == Qt.Key_L:
                    self.control_thread.key = key
                else:
                    if key == Qt.Key_W:
                        self.tello.send_rc_control(0, -10, 0, 0)
                    if key == Qt.Key_A:
                        self.tello.send_rc_control(-10, 0, 0, 0)
                    if key == Qt.Key_S:
                        self.tello.send_rc_control(0, 10, 0, 0)
                    if key == Qt.Key_D:
                        self.tello.send_rc_control(10, 0, 0, 0)
            if self.control_mode == 1:
                self.ui.statusbar.showMessage(lut_key(key)+'...')
                self.control_thread.key = key

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if event.isAutoRepeat():
            pass
        else:
            key = event.key()
            key_list = [Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D]
            if self.control_mode == 0:
                if key in key_list:
                    self.tello.send_rc_control(0, 0, 0, 0)

    def connect_tello(self):
        self.tello = Tello()
        self.my_thread = FrameThread(self.tello)

        self.tello_queue = queue.Queue()
        self.tello_queue.maxsize = 1
        self.control_thread = ControlThread(self.tello, self.tello_queue)
        self.my_thread.signal.connect(self.set_template)
        self.my_thread.start()
        self.control_thread.start()

        self.control_thread.signal.connect(self.show_state)

    def take_photo(self):
        cv2.imwrite("test.jpg", self.my_thread.img)

    def set_control_mode(self, mode: int):
        self.control_mode = mode
        print(mode)

    def show_state(self, key: int):
        self.ui.statusbar.showMessage(lut_key(key)+' OK', 2000)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()

    sys.exit(app.exec())
