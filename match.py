import cv2  
import imutils
import numpy as np
import time
start =time.perf_counter()
# CV_TM_SQDIFF 平方差匹配法：该方法采用平方差来进行匹配；最好的匹配值为0；匹配越差，匹配值越大。
# CV_TM_CCORR 相关匹配法：该方法采用乘法操作；数值越大表明匹配程度越好。
# CV_TM_CCOEFF 相关系数匹配法：1表示完美的匹配；-1表示最差的匹配。
# CV_TM_SQDIFF_NORMED 归一化平方差匹配法
# CV_TM_CCORR_NORMED 归一化相关匹配法
# CV_TM_CCOEFF_NORMED 归一化相关系数匹配法
template=cv2.imread("target3.jpg")
image=cv2.imread("2.2.jpg")
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
value=0
flag=0
for scale in np.linspace(0.1, 0.15, 10)[::-1]:
        print ("scale",scale)
        # 根据scale比例缩放图像，并保持其宽高比
        resized = imutils.resize(template, width=int(template.shape[1] * scale))
        result = cv2.matchTemplate(image, resized, cv2.TM_CCOEFF)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(result)
        if(maxVal>value):
                value=maxVal
                point=maxLoc
                (tH, tW) = resized.shape[:2]
                flag=1
image1=image
if flag==1:
        cv2.rectangle(image1, (point[0], point[1]),
                 (point[0] + tW, point[1] + tH), (0, 0, 255), 2)
cv2.imshow("image",image1)
end = time.perf_counter()
print('Running time: %s Seconds'%(end-start))
cv2.waitKey()