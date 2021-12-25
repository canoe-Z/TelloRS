import time
import cv2
import numpy as np
import torch

import os  # noqa
import sys  # noqa
# sys.path.append(os.path.join(os.path.dirname(__file__), "nanodet"))  # noqa

# from nanodet.data.batch_process import stack_batch_img
# from nanodet.data.collate import naive_collate
# from nanodet.data.transform import Pipeline
# from nanodet.model.arch import build_model
# from nanodet.util import Logger, cfg, load_config, load_model_weight
# from nanodet.util.path import mkdir


class Nanodet(object):
    def __init__(self, device="cpu"):
        # 初始化
        local_rank = 0
        torch.backends.cudnn.enabled = True
        torch.backends.cudnn.benchmark = True

        # 获得当前程序的绝对路径
        self.abs_path = os.path.dirname(__file__)
        # 配置文件路径
        config_path = os.path.join(
            self.abs_path, "nanodet", "config", "nanodet-m-416.yml")
        # 模型路径
        model_path = os.path.join(self.abs_path, "model", "model_best.pth")

        load_config(cfg, config_path)
        logger = Logger(local_rank, use_tensorboard=False)

        self.cfg = cfg
        self.device = device
        model = build_model(cfg.model)
        ckpt = torch.load(
            model_path, map_location=lambda storage, loc: storage)
        load_model_weight(model, ckpt, logger)
        if cfg.model.arch.backbone.name == "RepVGG":
            deploy_config = cfg.model
            deploy_config.arch.backbone.update({"deploy": True})
            deploy_model = build_model(deploy_config)
            from nanodet.model.backbone.repvgg import repvgg_det_model_convert

            model = repvgg_det_model_convert(model, deploy_model)
        self.model = model.to(device).eval()
        self.pipeline = Pipeline(
            cfg.data.val.pipeline, cfg.data.val.keep_ratio)

    # 设定要检测的目标标号
    def set_target(self, target_id):
        self.target_id = target_id

    # 传入一张图片 预测检测框位置
    def detect(self, img):
        img_info = {"id": 0}
        height, width = img.shape[:2]
        img_info["height"] = height
        img_info["width"] = width

        meta = dict(img_info=img_info, raw_img=img, img=img)
        meta = self.pipeline(None, meta, self.cfg.data.val.input_size)
        meta["img"] = torch.from_numpy(
            meta["img"].transpose(2, 0, 1)).to(self.device)
        meta = naive_collate([meta])
        meta["img"] = stack_batch_img(meta["img"], divisible=32)
        with torch.no_grad():
            results = self.model.inference(meta)
        # 获得所有检测框
        all_box, prob = self.get_boxes(results[0], 0.5)

        return all_box, prob

    # 获得检测框，检测框变成整形 (x1,y1,w,h)的形式 同时只取给定的目标类型的检测框
    def get_boxes(self, dets, score_thresh):
        all_box = []
        prob = []
        for label in dets:
            # 筛选指定目标
            # if label == self.target_id:
            for bbox in dets[label]:
                score = bbox[-1]
                if score > score_thresh:
                    x0, y0, x1, y1 = [int(i) for i in bbox[:4]]
                    all_box.append([x0, y0, abs(x1 - x0), abs(y1 - y0)])
                    prob.append(score)
        return np.array(all_box, dtype=np.int), np.array(prob)

    # 画检测框
    def draw_boxes(self, img, all_box, prob):
        for bbox, score in zip(all_box, prob):
            [x, y, w, h] = bbox
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.putText(img, '%.2f' %
                        score, (x, y - 5), 0, 0.7, (0, 255, 0), 2)
            # cv2.putText(img, str(self.target_id),
            #             (x, y - 25), 0, 0.7, (0, 255, 0), 2)
        return img


def main():
    predictor = Nanodet()
    predictor.set_target(0)
    cap = cv2.VideoCapture("./data/test_video.mp4")
    cv2.namedWindow("detect")
    while cap.isOpened():
        _, frame = cap.read()
        start = time.perf_counter()
        all_box, prob = predictor.detect(frame)
        frame = predictor.draw_boxes(frame, all_box, prob)
        end = time.perf_counter()
        time1 = (end - start) * 1000.
        print("forward time:%fms" % time1)
        cv2.imshow("detect", frame)
        if cv2.waitKey(30) == 27:
            break

    # img = cv2.imread("../../test.jpg")
    # import time
    # start = time.perf_counter()
    # meta, res = predictor.inference(img)
    # end = time.perf_counter()
    # time = (end - start) * 1000.
    # print("forward time:%fms"%time)
    # print(type(res))


if __name__ == "__main__":
    main()
