from PySide6 import QtGui


def cv2toQImage(img):
    height, width, _ = img.shape
    bytesPerLine = 3 * width
    qImg = QtGui.QImage(img.data, width, height,
                        bytesPerLine, QtGui.QImage.Format_BGR888)
    return qImg
