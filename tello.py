from djitellopy import Tello
import cv2
tello = Tello()

tello.connect()
x=tello.get_acceleration_x()
y=tello.get_acceleration_y()
z=tello.get_acceleration_z()
print(x,y,z)
print(tello.get_battery())


tello.streamon()
frame_read = tello.get_frame_read()
tello.takeoff()
tello.move_up(50)

# while True:
#     # In reality you want to display frames in a seperate thread. Otherwise
#     #  they will freeze while the drone moves.
#     # 在实际开发里请在另一个线程中显示摄像头画面，否则画面会在无人机移动时静止
#     img = frame_read.frame
#     cv2.imshow("drone", img)

#     key = cv2.waitKey(1) & 0xff
#     if key == 27: # ESC
#         break
#     elif key == ord('w'):
#         tello.move_forward(30)
#     elif key == ord('s'):
#         tello.move_back(30)
#     elif key == ord('a'):
#         tello.move_left(30)
#     elif key == ord('d'):
#         tello.move_right(30)
#     elif key == ord('e'):
#         tello.rotate_clockwise(30)
#     elif key == ord('q'):
#         tello.rotate_counter_clockwise(30)
#     elif key == ord('r'):
#         tello.move_up(30)
#     elif key == ord('f'):
#         tello.move_down(30)
#     i=0
#     cv2.imwrite(str(i)+".jpg",img)
#     i=i+1
# tello.land()

for i in range(13):
    tello.move_forward(30)
    img=frame_read.frame
    cv2.waitKey(1)
    cv2.imwrite(str(i)+".jpg",img)
tello.rotate_counter_clockwise(90)
tello.move_forward(30)
tello.rotate_counter_clockwise(90)
img=frame_read.frame
cv2.waitKey(1)
cv2.imwrite("13.jpg",img)
for i in range(14,25):
    tello.move_forward(30)
    img=frame_read.frame
    cv2.waitKey(1)
    cv2.imwrite(str(i)+".jpg",img)
tello.land()