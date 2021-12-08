import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QThread, Signal
from Ui_untitled import Ui_MainWindow
import cv2

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.my_thread = MyThread()
        self.my_thread.my_signal.connect(self.set_label_func)  # 3

    def buttonClicked(self):
        print("1")

    def count_func(self):
        self.my_thread.start()

    def set_label_func(self, num):  # 4
        print(num)
        print(self.my_thread.count)
        # img2
        # #self.label.setText(num)
        # _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QtGui.QImage.Format_RGB888) #pyqt5转换成自己能放的图片格式
        # jpg_out = QtGui.QPixmap(_image).scaled(self.imgLabel.width(), self.imgLabel.height()) #设置图片大小
        # self.imgLabel.setPixmap(jpg_out) #设置图片显示




class MyThread(QThread):
    my_signal = Signal(str)     # 1

    def __init__(self):
        super(MyThread, self).__init__()
        self.count = 0

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
        # get a frame
            _, self.frame = cap.read()
            # show a frame
            #cv2.imshow("capture", frame)
            #self.sleep(1)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
        # while True:
        #     print(self.count)
            self.count += 1
            self.my_signal.emit(str(self.count))  # 2
            #self.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec())
