import cv2

img = cv2.imread("match/map.png")
xmin = 10
xmax = 100
ymin = 10
ymax = 20
cv2.rectangle(img, (xmin, ymin), (xmax, ymax),
              (0, 0, 255), thickness=3)
cv2.namedWindow('test')
cv2.imshow('test', img[ymin:ymax, xmin:xmax])

cv2.waitKey()
