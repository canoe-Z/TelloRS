from time import sleep
from djitellopy import Tello
from icecream import ic
from time import time


if __name__ == '__main__':
    tello = Tello()
    tello.connect()
    tello.set_video_bitrate(Tello.BITRATE_5MBPS)
    tello.set_video_resolution(Tello.RESOLUTION_720P)
    tello.set_video_fps(Tello.FPS_30)
    last_time = time()
    x, y, z = 0, 0, 0
    while True:
        #tello.send_command_without_return("keepalive")
        #tello.send_control_command("keepalive")
        # ax, ay, az = tello.get_acceleration_x(
        # ), tello.get_acceleration_y(), tello.get_acceleration_z()
        ##print(ax, ay, az)
        #vx, vy, vz = tello.get_speed_x(), tello.get_speed_y(), tello.get_speed_z()
        vx = tello.get_speed_x()
        currnet_time = time()
        delta_time = currnet_time-last_time
        last_time = currnet_time
        delta_x = vx*delta_time
        #delta_x, delta_y, delta_z = vx*delta_time, vy*delta_time, vz*delta_time
        x += delta_x
        #y += delta_y
        #z += delta_z
        print(vx)  # , vy, vz)  # delta_z)
        #print(x, y, z)
        # sleep(0.1)
        # print('##########################')
        # ic(tello.get_battery())
        # ic(tello.get_barometer())
        # ic(tello.get_distance_tof())
        # ic(tello.get_height())
        # ic(tello.get_speed_x(), tello.get_speed_y(), tello.get_speed_z())
        # ic(time())
        # sleep(3)
