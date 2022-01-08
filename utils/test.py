import cv2
import numpy as np


def form_size(src):  #  src输入的图片,返回修改后的图片
    win_width, win_height = 800, 600   #  ui界面窗口尺寸，自行修改
    dst = np.zeros((win_height, win_width, 3), np.uint8)
    src_height, src_width = src.shape[:2]
    if src_width / src_height > win_width / win_height:
        re_width, re_height = win_width, int(src_height * win_width / src_width)
        resize_image = cv2.resize(src, (re_width, re_height), interpolation=cv2.INTER_LINEAR)
        for i in range(re_height):
            for j in range(re_width):
                for k in range(3):
                    dst[i + int((win_height - re_height) / 2), j, k] = resize_image[i, j, k]
    else:
        re_width, re_height = int(src_width * win_height / src_height), win_height
        resize_image = cv2.resize(src, (re_width, re_height), interpolation=cv2.INTER_LINEAR)
        for i in range(re_height):
            for j in range(re_width):
                for k in range(3):
                    dst[i, j + int((win_width - re_width) / 2), k] = resize_image[i, j, k]
    return dst


src = cv2.imread(r'data\18_21_39_2021_12_14.png')
dst = form_size(src)
cv2.namedWindow('dst')
cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
