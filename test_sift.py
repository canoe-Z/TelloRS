import cv2
import numpy as np
import time


def match(img1, img2):
    # find the keypoints and descriptors with SIFT
    MIN_MATCH_COUNT = 5
    sift = cv2.SIFT_create()
    # sift=cv2.ORB_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=2)
    search_params = dict(checks=2)

    #flann = cv2.FlannBasedMatcher(index_params, search_params)
    #matches = flann.knnMatch(des1, des2, k=2)

    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.9*n.distance:
            good.append(m)
    print(len(good))
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 3.0)
        matchesMask = mask.ravel().tolist()

        h, w = img1.shape[:2]
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1],
                         [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        points = np.int32(dst)
        # print(points)
        img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 5, cv2.LINE_8)

        M = cv2.moments(points)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        img2 = cv2.circle(img2, (cx, cy), 4, (0, 255, 255), 10)
        #cv2.namedWindow("t", cv2.WINDOW_NORMAL)
        #cv2.imshow("t", img2)

    else:
        print("Not enough matches are found - %d/%d" %
              (len(good), MIN_MATCH_COUNT))
        matchesMask = None
    print('1')
    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)

    img3 = cv2.drawMatches(
        img1, kp1, img2[:, :, :3], kp2, good, None, **draw_params)
    img3 = cv2.putText(img3, str(1)+' East', (10, 1720),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    img3 = cv2.putText(img3, str(2)+' North', (10, 1650),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    #nigg = cv2.cvtColor(img3, cv2.COLOR_RGB2BGR)
    # cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    # cv2.imshow("Frame", img3)
    # cv2.waitKey()
    return img2
    #key = cv2.waitKey(1) & 0xFF


if __name__ == '__main__':
    img1 = cv2.imread('./data/target3.jpg')
    img2 = cv2.imread('./data/moban.jpg')
    start = time.perf_counter()
    match(img1, img2)
    end = time.perf_counter()
    print(end-start)
    np.hstack()
