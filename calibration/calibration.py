import cv2 as cv
import numpy as np
import glob
import os

if __name__ == '__main__':
    # 循环中断
    criteria = (cv.TERM_CRITERIA_EPS+cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # 标定板交叉点的个数
    row = 11
    column = 8
    objp = np.zeros((row*column, 3), np.float32)
    objp[:, :2] = np.mgrid[0:row, 0:column].T.reshape(-1, 2)

    objpoints = []  # 实际空间3D点
    imgpoints = []  # 图像中2D点

    # 批量读取图片
    images = glob.glob('./data/calibration_image/*.jpg')
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # 找标定板角点
        ret, corners = cv.findChessboardCorners(gray, (row, column), None)

        if ret == True:
            objpoints.append(objp)

            corners2 = cv.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

    # 标定相机
    ret, Matrix, dist, rvecs, tvecs = cv.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)

    datadir = "./data/pai1"

    path = os.path.join(datadir)
    img_list = os.listdir(path)

    for i in img_list:
        img = cv.imread(os.path.join(path, i))
        h, w = img.shape[:2]
        newMatrix, roi = cv.getOptimalNewCameraMatrix(
            Matrix, dist, (w, h), 1, (w, h))  # 矫正图像

        dst = cv.undistort(img, Matrix, dist, None, newMatrix)
        dst = dst[30:-30, 20:-20, :]
        cv.imwrite('./data/result2/'+i, dst)

    # 计算重投影误差
    tot_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv.projectPoints(
            objpoints[i], rvecs[i], tvecs[i], Matrix, dist)
        error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
        tot_error += error

    # 输出参数
    print('ret:\n', ret)
    print('mtx:\n', Matrix)
    print('dist:\n', dist)
    print('rvecs:\n', rvecs)
    print('tvecs:\n', tvecs)
    print("total error: ", tot_error/len(objpoints))
