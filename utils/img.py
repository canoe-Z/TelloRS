from PySide6 import QtGui
from numpy import ndarray


def cv2toQImage(img: ndarray):
    height, width, _ = img.shape
    bytesPerLine = 3 * width
    qImg = QtGui.QImage(img.data, width, height,
                        bytesPerLine, QtGui.QImage.Format_BGR888)
    return qImg
