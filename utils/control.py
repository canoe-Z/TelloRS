from PySide6.QtCore import Qt


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
