import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal
from Ui_untitled import Ui_MainWindow
from djitellopy import Tello
import numpy as np


tello = Tello()
tello.connect()

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.my_thread = MyThread()
        self.test_thread=TestThread()
        self.test1_thread=TestThread1()
        self.test2_thread=TestThread2()
        self.test3_thread=TestThread3()
        self.test4_thread=TestThread4()
        self.test5_thread=TestThread5()
        self.my_thread.my_signal.connect(self.set_label_func)  # 3
        self.my_thread.start()
        

    def count_func(self):
        self.my_thread.start()

    def set_label_func(self):
        qImg = self.my_thread.qImg
        qImg = QtGui.QPixmap(qImg).scaled(
            self.label.width(), self.label.height())  # 设置图片大小
        self.label.setPixmap(qImg)  # 设置图片显示

    # 重新实现各事件处理程序
    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        if key==Qt.Key_T:
            #tello.takeoff()
            self.test_thread.start()
        if key==Qt.Key_W:
            #tello.takeoff()
            self.test1_thread.start()
        if key==Qt.Key_A:
            #tello.takeoff()
            self.test2_thread.start()
        if key==Qt.Key_S:
            #tello.takeoff()
            self.test3_thread.start()
        if key==Qt.Key_D:
            #tello.takeoff()
            self.test4_thread.start()
        if key==Qt.Key_L:
            #tello.takeoff()
            self.test5_thread.start()


class MyThread(QThread):
    my_signal = Signal()     # 1

    def __init__(self):
        super(MyThread, self).__init__()

        tello.streamon()
        self.frame_read = tello.get_frame_read()

    def run(self):
        while True:
            # get a frame
            img = self.frame_read.frame
            a = img*2
            height, width, channel = img.shape
            bytesPerLine = 3 * width
            self.qImg = QtGui.QImage(img.data, width, height,
                                     bytesPerLine, QtGui.QImage.Format_BGR888)
            self.my_signal.emit()
            #self.sleep(0.1)



class TestThread(QThread):
    #my_signal = Signal()     # 1

    def __init__(self):
        super(TestThread, self).__init__()

    def run(self):
        tello.takeoff()

class TestThread1(QThread):
    #my_signal = Signal()     # 1

    def __init__(self):
        super(TestThread1, self).__init__()

    def run(self):
        tello.move_forward(30)

class TestThread2(QThread):
    #my_signal = Signal()     # 1

    def __init__(self):
        super(TestThread2, self).__init__()

    def run(self):
        tello.move_left(30)

class TestThread3(QThread):
    #my_signal = Signal()     # 1

    def __init__(self):
        super(TestThread3, self).__init__()

    def run(self):
        tello.move_back(30)

class TestThread4(QThread):
    #my_signal = Signal()     # 1

    def __init__(self):
        super(TestThread4, self).__init__()

    def run(self):
        tello.move_right(30)

class TestThread5(QThread):
    #my_signal = Signal()     # 1

    def __init__(self):
        super(TestThread5, self).__init__()

    def run(self):
        tello.land()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()

    sys.exit(app.exec())
