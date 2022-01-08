import cv2
import sys

from det.nanodet_plus import NanoDetPlus
from simple_pid import PID
import time


class XModel(object):
    def __init__(self, distance):
        self.distance = distance
        self.scale = 0.00001

    def update(self, x_move, dt):
        if x_move >= 0:
            self.distance -= self.scale * x_move * dt
        else:
            self.distance += self.scale * x_move * dt
        return self.distance


class YModel(object):
    def __init__(self, distance):
        self.distance = distance
        self.scale = 0.00001

    def update(self, y_move, dt):
        if y_move >= 0:
            self.distance -= self.scale * y_move * dt
        else:
            self.distance += self.scale * y_move * dt
        return self.distance


##############################################################
minsize = 7000  # 框的最小尺寸，若小于这个尺寸则下一次也是 “识别” 而非 “跟踪”
##############################################################
##############################################################

tracker = cv2.TrackerCSRT_create()
video = cv2.VideoCapture(
    r'D:\tello_tracking\tello_tracking\video\video_test\tello1.mp4')
if not video.isOpened():
    print("Could not open video")
    sys.exit()
model = NanoDetPlus('./det/model/nanodet_car.onnx')
i = 0
track_flag = 0
while True:
    ok, frame = video.read()
    if ok is None or frame is None:
        break
    else:
        i += 1

    if i == 1:
        box = model.detect2(frame)
        if(len(box) == 0):
            i = 0
            cv2.putText(frame, "Tracking failure detected", (100, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            continue
        ok = tracker.init(frame, box)
        if not ok:
            continue
    success, bbox = tracker.update(frame)

    centerx = int(bbox[0]+(bbox[2])/2)
    centery = int(bbox[1]+(bbox[3])/2)
    if(frame[centery, centerx, 0] <= 150 and frame[centery, centerx, 1] <= 150 and frame[centery, centerx, 2] <= 150):
        success = 0

    if success:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        i = 0
    if(box[2]*box[3] < minsize):
        print("框较小")
        i = 0

    # if track_flag == 0:
    #     x_distance = centerx - frame.shape[1] / 2
    #     y_distance = centery - frame.shape[0] / 2
    #     x_model = XModel(x_distance)
    #     y_model = YModel(y_distance)
    #     x_pid = PID(0.001, 0.1, 0.05, setpoint=1)
    #     y_pid = PID(0.001, 0.05, 0.01, setpoint=1)
    #     start_time = time.time()
    #     last_time = start_time
    #     track_flag = 1
    # else:
    #     x_distance = centerx - frame.shape[1] / 2
    #     y_distance = centery - frame.shape[0] / 2
    #     #print(x_distance,y_distance)
    #     current_time = time.time()
    #     dt = current_time - last_time
    #     last_time = current_time

    #     x_move = x_pid(x_distance)
    #     y_move = y_pid(y_distance)
    #     #print(x_move,y_move)
    #     x_distance = x_model.update(x_move, dt)
    #     #print('x_distance: ', x_distance)
    #     y_distance = y_model.update(y_move, dt)
    #     #print('y_distance: ', y_distance)
    #     if x_distance <= 4 and y_distance <= 4:
    #         break
    x_distance = centerx - frame.shape[1] / 2
    y_distance = centery - frame.shape[0] / 2
    x_model = XModel(x_distance)
    y_model = YModel(y_distance)
    x_pid = PID(0.001, 0.1, 0.05, setpoint=1)
    y_pid = PID(0.001, 0.05, 0.01, setpoint=1)
    start_time = time.time()
    last_time = start_time
    while True:
        current_time = time.time()
        dt = current_time - last_time
        x_move = x_pid(x_distance)
        y_move = y_pid(y_distance)
        x_distance = x_model.update(x_move, dt)
        #print('x_distance: ', x_distance)
        y_distance = y_model.update(y_move, dt)
        print(x_move, y_move)
        '''
        if x_move <= 0:
            drone.send_command('right' + ' ' + str(-x_move))
        else:
            drone.send_command('left' + ' ' + str(x_move))
        '''
        # if y_move >= 0:
        #     drone.send_command('back' + ' ' + str(y_move))
        # else:
        #     drone.send_command('forward' + ' ' + str(-y_move))

        if x_distance <= 4 and y_distance <= 4:
            break
    break
        # if end_tracking:
        #     break
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) < 1:
        break

video.release()
cv2.destroyAllWindows()
