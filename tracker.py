import sys
import cv2
from det.nanodet_plus import NanoDetPlus


class Tracker(object):
    def __init__(self):
        self.tracker = cv2.TrackerCSRT_create()
        # video = cv2.VideoCapture(
        #     r'C:\Users\Ryuhiu\Desktop\TelloRS-main\tello2_Trim_Trim.mp4')
        # if not video.isOpened():
        #     print("Could not open video")
        #     sys.exit()
        self.model = NanoDetPlus('./det/model/nanodet_car.onnx', ['car'])
        self.model.prob_threshold = 0.6

        self.flag = 0  # flag为0时识别，flag为1时跟踪,初始时先识别为0
        self.row = 0  # 记录当前循环的轮数

    def update(self, frame):
        success_flag = False
        centerx = 0
        centery = 0
        self.row += 1  # 轮数+1
        if(self.row % 10 == 0):  # 每隔10帧，就让flag变回0，即：本次为识别而非跟踪
            self.flag = 0
        if self.flag == 0:  # 如果flag为0，则进行识别
            self.flag = 1  # 改成1，下次就可以变成跟踪了
            # box是识别到的小车信息，四个数据分别是：y，x，宽，长（矩阵坐标系）
            box = self.model.detect2(frame)
            if(len(box) == 0):  # 如果没有识别到小车，本次循环结束
                # 没有识别到小车，在循环结束前也要注意更新imshow
                # 不然图片会由此卡住直到检测到小车为止
                # 此外也标记一下没检测成功
                cv2.putText(frame, "Tracking failure detected", (100, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                self.flag = 0  # 由于识别失败，下次还是识别
                return frame, success_flag, centerx, centery

            self.tracker.init(frame, box)
            # ok = self.tracker.init(frame, box)#把box赋给跟踪有关？？
            # if not ok:#似乎没啥太大用处，应该不会失败
            #     return frame
        # 虽然我也不知道update是啥玩意，可能是为了防止box超出图片的边界？？
        success, box = self.tracker.update(frame)

        centerx = int(box[0]+(box[2])/2)  # 求出框的中心位置
        centery = int(box[1]+(box[3])/2)
        if(frame[centery, centerx, 0] <= 150 and frame[centery, centerx, 1] <= 150 and frame[centery, centerx, 2] <= 150):
            success = 0  # 如果框中心不是白色，就使得success为0

        if success:  # 如果一切顺利，就把框画在图上
            p1 = (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:  # success为0，即中心框不是白色，则跟踪失败，下一回合是识别
            self.flag = 0
        success_flag = True
        return frame, success_flag, centerx, centery


# video = cv2.VideoCapture(
#     r'D:\tello_tracking\tello_tracking\video\video_test\tello2.mp4')
# if not video.isOpened():
#     print("Could not open video")
#     sys.exit()
# tracker = Tracker()
# while True:
#     ok, frame = video.read()
#     if ok is None or frame is None:
#         break
#     output, _, _, _ = tracker.update(frame)
#     cv2.imshow("Frame", output)
#     key = cv2.waitKey(1) & 0xFF
#     if cv2.getWindowProperty('Frame', cv2.WND_PROP_VISIBLE) < 1:
#         break
