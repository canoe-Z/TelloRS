import cv2
import imutils
import numpy as np
import time

# def getNextMinLoc(result, maxLoc, templatW, templatH):
#     startX = maxLoc[0]
#     startY = maxLoc[1]
#     endX = maxLoc[0] + templatW
#     endY = maxLoc[1] + templatH
#     if(startX < 0 | startY < 0):
#         startX = 0
#         startY = 0
#     if(endX > result[0] - 1 | endY > result[1] - 1):
#         endX = result[0] - 1
#         endY = result[1] - 1
#     for i in range (startX,endX):
#         for j in range(startY,endY):
#             result[i,j]=0
#     (new_minVal, new_maxVal, new_minLoc, new_maxLoc) = cv2.minMaxLoc(result)
#     return result,new_maxLoc,new_maxVal


def draw(image, template, threshold):
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    (tW, tH) = template.shape[:2]
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + tW, pt[1] + tH), (0, 0, 255), 2)


if __name__ == '__main__':
    start = time.perf_counter()
    # CV_TM_SQDIFF 平方差匹配法：该方法采用平方差来进行匹配；最好的匹配值为0；匹配越差，匹配值越大。
    # CV_TM_CCORR 相关匹配法：该方法采用乘法操作；数值越大表明匹配程度越好。
    # CV_TM_CCOEFF 相关系数匹配法：1表示完美的匹配；-1表示最差的匹配。
    # CV_TM_SQDIFF_NORMED 归一化平方差匹配法
    # CV_TM_CCORR_NORMED 归一化相关匹配法
    # CV_TM_CCOEFF_NORMED 归一化相关系数匹配法
    template1 = cv2.imread("./output/oil.png")
    template2 = cv2.imread("./output/oil1.png")
    template3 = cv2.imread("./output/airplane.png")
    template4 = cv2.imread("./output/airplane1.png")
    template5 = cv2.imread("./output/airplane2.png")
    template6 = cv2.imread("./output/airplane3.png")
    template7 = cv2.imread("./output/airplane4.png")
    image = cv2.imread("./output/18_22_07_2021_12_14.png")
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    threshold = 0.79
    draw(image, template1, threshold)
    draw(image, template2, threshold)
    draw(image, template3, threshold)
    draw(image, template4, threshold)
    draw(image, template5, threshold)
    draw(image, template6, threshold)
    draw(image, template7, threshold)
    cv2.imshow("image", image)
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end-start))
    cv2.waitKey()

    # value = 0
    # flag = 0
    # for scale in np.linspace(0.1, 0.5, 10)[::-1]:
    #     print("scale", scale)
    #     # 根据scale比例缩放图像，并保持其宽高比
    #     resized = imutils.resize(template, width=int(template.shape[1] * scale))
    #     result = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF)
    #     (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
    #     if(maxVal > value):
    #         value = maxVal
    #         point = maxLoc
    #         (tH, tW) = resized.shape[:2]
    #         flag = 1
    # image1 = image
    # if flag == 1:
    #     cv2.rectangle(image1, (point[0], point[1]),
    #                   (point[0] + tW, point[1] + tH), (0, 0, 255), 2)
    # cv2.imshow("image", image1)
    # end = time.perf_counter()
    # print('Running time: %s Seconds' % (end-start))
    # cv2.waitKey()
