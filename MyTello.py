from djitellopy import Tello
from PySide6.QtCore import Qt


class MyTello(Tello):
    # RETRY_COUNT = 3  # number of retries after a failed command
    # TELLO_IP = '192.168.10.1'  # Tello IP address

    # def __init__(self):
    #     super(MyTello,self).__init__(
    #         self,
    #         host='192.168.10.1',
    #         retry_count=3)

    def rc_control_by_key(self, key: int, move_speed: int):
        if key == Qt.Key_W:
            self.send_rc_control(0, move_speed, 0, 0)
        if key == Qt.Key_A:
            self.send_rc_control(-move_speed, 0, 0, 0)
        if key == Qt.Key_S:
            self.send_rc_control(0, -move_speed, 0, 0)
        if key == Qt.Key_D:
            self.send_rc_control(move_speed, 0, 0, 0)
