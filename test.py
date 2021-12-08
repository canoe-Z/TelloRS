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
        # if Qt.Key_A <= key <= Qt.Key_Z:
        #     if event.modifiers() & Qt.ShiftModifier:  # Shift 键被按下
        #         self.statusBar().showMessage('"Shift+%s" pressed' % chr(key), 500)
        #     elif event.modifiers() & Qt.ControlModifier:  # Ctrl 键被按下
        #         self.statusBar().showMessage('"Control+%s" pressed' % chr(key), 500)
        #     elif event.modifiers() & Qt.AltModifier:  # Alt 键被按下
        #         self.statusBar().showMessage('"Alt+%s" pressed' % chr(key), 500)
        #     else:
        #         self.statusBar().showMessage('"%s" pressed' % chr(key), 500)

        # elif key == Qt.Key_Home:
        #     self.statusBar().showMessage('"Home" pressed', 500)
        # elif key == Qt.Key_End:
        #     self.statusBar().showMessage('"End" pressed', 500)
        # elif key == Qt.Key_PageUp:
        #     self.statusBar().showMessage('"PageUp" pressed', 500)
        # elif key == Qt.Key_PageDown:
        #     self.statusBar().showMessage('"PageDown" pressed', 500)
        # # else:   #其它未设定的情况
        #     # QWidget.keyPressEvent(self, event)  #留给基类处理


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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()

    sys.exit(app.exec())
