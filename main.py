import sys
import queue
from djitellopy import Tello
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal

from ui.Ui_untitled import Ui_MainWindow
from utils.img import cv2toQImage

from tello import MyThread, TestThread


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

        self.tello = Tello()
        self.my_thread = MyThread(self.tello)

        self.tello_queue = queue.Queue()
        self.test_thread = TestThread(self.tello, self.tello_queue)
        self.my_thread.signal.connect(self.set_image)

        self.my_thread.start()
        self.test_thread.start()

    def count_func(self):
        self.my_thread.start()

    def set_image(self):
        qImg = cv2toQImage(self.my_thread.img)
        qImg = QtGui.QPixmap(qImg).scaled(
            self.label.width(), self.label.height())  # 设置图片大小
        self.label.setPixmap(qImg)  # 设置图片显示

    # 重新实现各事件处理程序
    def keyPressEvent(self, event):
        self.tello_queue.put(event.key())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()

    sys.exit(app.exec())
