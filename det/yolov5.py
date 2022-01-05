import onnxruntime
import cv2
import torch
import time
import numpy as np
import argparse
from det.yolov5_utils import *


class YOLOv5(object):
    def __init__(self, input_shape=320, prob_threshold=0.4, iou_threshold=0.3):
        stride, names = 64, [
            f'class{i}' for i in range(1000)]  # assign defaults
        self.prob_threshold = prob_threshold
        self.iou_threshold = iou_threshold
        self.session = onnxruntime.InferenceSession('./det/model/yolov5n.onnx')

    def detect(self, img):
        im = img.copy().astype('float32')

        # Padded resize
        im = letterbox(im, 320, stride=32, auto=False, scaleFill=False)[0]
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB

        im /= 255  # 0 - 255 to 0.0 - 1.0
        im = im[None]  # expand for batch dim

        y = self.session.run([self.session.get_outputs()[0].name], {
            self.session.get_inputs()[0].name: im})[0]
        y = torch.tensor(y)

        pred = non_max_suppression(y, self.prob_threshold, self.iou_threshold)
        for i, det in enumerate(pred):
            det[:, :4] = scale_coords(
                im.shape[2:], det[:, :4], img.shape).round()
            det = det.cpu().numpy()
            for bbox in det:
                bx, by, bw, bh, conf, _ = bbox
                c1, c2 = ((int(bx), int(by)), (int(bw), int(bh)))
                cv2.rectangle(img, c1, c2, (0, 0, 255),
                              5, cv2.LINE_AA)  # filled
        return img


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str,
                        default='bus.jpg', help="image path")
    parser.add_argument('--input_shape', default=320, type=int,
                        choices=[320, 416], help='input image shape')
    parser.add_argument('--confThreshold', default=0.35,
                        type=float, help='class confidence')
    parser.add_argument('--nmsThreshold', default=0.6,
                        type=float, help='nms iou thresh')
    args = parser.parse_args()

    srcimg = cv2.imread(args.imgpath)
    net = YOLOv5(input_shape=args.input_shape,
                 prob_threshold=args.confThreshold, iou_threshold=args.nmsThreshold)

    import time
    #while True:
    a = time.time()
    result = net.detect(srcimg)
    b = time.time()
    print('waste time', b-a)

    winName = 'Deep learning object detection in OpenCV'
    cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
    cv2.imshow(winName, srcimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
