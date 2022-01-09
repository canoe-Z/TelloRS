import imp
import os
import sys

from PySide6.QtCore import Qt
from djitellopy import Tello


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


def send_rc_control_by_key(tello: Tello, key: int, rc_speed: int):
    if key == Qt.Key_W:
        tello.send_rc_control(0, rc_speed, 0, 0)
    if key == Qt.Key_A:
        tello.send_rc_control(-rc_speed, 0, 0, 0)
    if key == Qt.Key_S:
        tello.send_rc_control(0, -rc_speed, 0, 0)
    if key == Qt.Key_D:
        tello.send_rc_control(rc_speed, 0, 0, 0)
    if key == Qt.Key_E:
        tello.send_rc_control(0, 0, 0, -rc_speed)
    if key == Qt.Key_Q:
        tello.send_rc_control(0, 0, 0, rc_speed)
    if key == Qt.Key_R:
        tello.send_rc_control(0, 0, -rc_speed, 0)
    if key == Qt.Key_F:
        tello.send_rc_control(0, 0, rc_speed, 0)
