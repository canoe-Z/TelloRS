import imp
import os
import sys

from PySide6.QtCore import Qt


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def lut_key(key: int) -> str:
    if key == Qt.Key_T:
        method = 'takeoff'
    if key == Qt.Key_W:
        method = 'move_forward'
    if key == Qt.Key_A:
        method = 'move_left'
    if key == Qt.Key_S:
        method = 'move_back'
    if key == Qt.Key_D:
        method = 'move_right'
    if key == Qt.Key_L:
        method = 'land'
    return method
