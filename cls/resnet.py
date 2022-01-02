from torchvision.datasets import ImageFolder
from torchvision import transforms as T
from torch.utils.data import DataLoader
from torchvision import models
import torch
import cv2
from PIL import Image
import onnxruntime
import numpy as np


class ResNet(object):
    def __init__(self):
        self.transform = T.Compose([
            # T.RandomResizedCrop(224),
            T.Resize((224, 224)),
            # T.RandomHorizontalFlip(),
            T.ToTensor(),
            T.Normalize(mean=[0.4, 0.4, 0.4], std=[0.2, 0.2, 0.2])
        ])

        onnx_model_path = "./cls/model/test2.onnx"
        self.resnet_session = onnxruntime.InferenceSession(onnx_model_path)

    def test(self, img):
        class_names = ['airport', 'building', 'forest', 'other', 'overpass',
                       'rectangular_farmland', 'sea', 'storage_tank']
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        input = self.transform(img).unsqueeze(0)

        inputs = {self.resnet_session.get_inputs()[0].name: input.numpy()}
        outs = self.resnet_session.run(None, inputs)[0]
        #input = input.to(self.device)
        # self.resnet18.eval()
        #output = self.resnet18(input)
        # print(output)
        # print(outs)
        result = class_names[np.argmax(outs)]
        return result
        #print('predicted:', result)


if __name__ == '__main__':
    model = ResNet()
    import time
    a = time.time()
    img = cv2.imread('./18_21_39_2021_12_14.png')
    #img = Image.open('./18_21_39_2021_12_14.png')
    result = model.test(img)
    b = time.time()
    print('waste time', b-a)
    print(result)
