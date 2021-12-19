import cv2
import numpy as np


class SIFT_matcher(object):
    def __init__(self, map):
        self.map = map
        self.sift = cv2.SIFT_create()
        self.kp_map, self.des_map = self.sift.detectAndCompute(map, None)
        self.MIN_MATCH_COUNT = 10

    def cal_rectangle_degree(self, img_ori, hull):
        # 计算该坐标点组成的四边形的面积
        im = np.zeros(img_ori.shape[:2], dtype="uint8")
        filling_image = np.array(
            [hull[0][0], hull[1][0], hull[2][0], hull[3][0]], np.int32)
        polygon_mask = cv2.fillPoly(im, [filling_image], 255)
        measure_polygon = np.sum(np.greater(polygon_mask, 0))

        # 计算该坐标点组成的四边形的外接矩形面积
        rect = cv2.minAreaRect(hull)  # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
        # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        box = cv2.convexHull(box, clockwise=True)
        filling_image = np.array(
            [box[0][0], box[1][0], box[2][0], box[3][0]], np.int32)
        rectangle_mask = cv2.fillPoly(im, [filling_image], 255)
        measure_rectangle = np.sum(np.greater(rectangle_mask, 0))

        # 计算矩形度
        Rectangle_degree = measure_polygon/measure_rectangle

        return Rectangle_degree

    def match(self, template):
        rectangle_degree = None
        center = None

        kp, des = self.sift.detectAndCompute(template, None)

        matcher = cv2.BFMatcher()
        matches = matcher.knnMatch(des, self.des_map, k=2)

        good_matches = []
        for m, n in matches:
            if m.distance < 0.85*n.distance:
                good_matches.append(m)

        if len(good_matches) > self.MIN_MATCH_COUNT:
            src_pts = np.float32(
                [kp[m.queryIdx].pt for m in good_matches]).reshape(-1, 2)
            dst_pts = np.float32(
                [self.kp_map[m.trainIdx].pt for m in good_matches]).reshape(-1, 2)

            H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 3.0)
            
            h, w = template.shape[:2]
            pts = np.float32([[0, 0], [0, h-1], [w-1, h-1],
                              [w-1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, H)
            points = np.int32(dst)
            rectangle_degree = self.cal_rectangle_degree(self.map, points)

            H = cv2.moments(points)
            cx = int(H['m10']/H['m00'])
            cy = int(H['m01']/H['m00'])
            center = (cx, cy)

        return len(good_matches), rectangle_degree, center


if __name__ == '__main__':
    img1 = cv2.imread('./data/target3.jpg')
    img2 = cv2.imread('./data/moban.jpg')

    sift_matcher = SIFT_matcher(img2)
    sift_matcher.match(img1)

    # if(rectangle_degree > 0.75):
    #     map = cv2.polylines(
    #         self.map, [np.int32(dst)], True, 255, 5, cv2.LINE_8)
    # else:
    #     print(rectangle_degree)

#map = cv2.circle(map, (cx, cy), 4, (0, 255, 255), 10)
    # print("Not enough matches are found - %d/%d" %
    #       (len(good_matches), MIN_MATCH_COUNT))
    #     matchesMask = None
    # draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
    #                    singlePointColor=None,
    #                    matchesMask=matchesMask,  # draw only inliers
    #                    flags=2)

    # img3 = cv2.drawMatches(
    #     template, kp, source[:, :, :3], kp2, good_matches, None, **draw_params)

    # cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    # cv2.imshow("Frame", map)
    # cv2.waitKey()
