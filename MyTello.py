from djitellopy import Tello


class MyTello(Tello):
    # RETRY_COUNT = 3  # number of retries after a failed command
    # TELLO_IP = '192.168.10.1'  # Tello IP address

    # def __init__(self):
    #     super(MyTello,self).__init__(
    #         self,
    #         host='192.168.10.1',
    #         retry_count=3)

    def move(self, direction: str, x: int) -> bool:
        return self.send_control_command("{} {}".format(direction, x))

    def move_left_return(self, x: int):
        """Fly x cm left.
        Arguments:
            x: 20-500
        """
        return self.move("left", x)

    def move_right_return(self, x: int):
        """Fly x cm right.
        Arguments:
            x: 20-500
        """
        return self.move("right", x)

    def move_forward_return(self, x: int):
        """Fly x cm forward.
        Arguments:
            x: 20-500
        """
        return self.move("forward", x)

    def move_back_return(self, x: int):
        """Fly x cm backwards.
        Arguments:
            x: 20-500
        """
        return self.move("back", x)

    def takeoff(self):
        return super().takeoff()
