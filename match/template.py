import cv2
import numpy as np
import time


class TemplateMatcher(object):
    def __init__(self, templates):
        self.templates = templates

    def detect(self, img, threshold=0.79):
        for template in self.templates:
            img = self.draw(img, template, threshold)
        return img

    def draw(self, image, template, threshold):
        # CV_TM_SQDIFF 平方差匹配法：该方法采用平方差来进行匹配；最好的匹配值为0；匹配越差，匹配值越大。
        # CV_TM_CCORR 相关匹配法：该方法采用乘法操作；数值越大表明匹配程度越好。
        # CV_TM_CCOEFF 相关系数匹配法：1表示完美的匹配；-1表示最差的匹配。
        # CV_TM_SQDIFF_NORMED 归一化平方差匹配法
        # CV_TM_CCORR_NORMED 归一化相关匹配法
        # CV_TM_CCOEFF_NORMED 归一化相关系数匹配法
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        (tW, tH) = template.shape[:2]
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image, pt, (pt[0] + tW, pt[1] + tH), (0, 0, 255), 2)
        return image


if __name__ == '__main__':
    start = time.perf_counter()

    template1 = cv2.imread("./output/oil.png")
    template2 = cv2.imread("./output/oil1.png")
    template3 = cv2.imread("./output/airplane.png")
    template4 = cv2.imread("./output/airplane1.png")
    template5 = cv2.imread("./output/airplane2.png")
    template6 = cv2.imread("./output/airplane3.png")
    template7 = cv2.imread("./output/airplane4.png")
    image = cv2.imread(r"output\20211227164046.png")

    predictor = TemplateMatcher(
        [template1, template2, template3, template4, template5, template6, template7])

    image = predictor.detect(image)
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", image)
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end-start))
    cv2.waitKey()
