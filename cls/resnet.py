import cv2
import numpy as np
import onnxruntime
from PIL import Image
from torchvision import transforms as T


class ResNet(object):
    def __init__(self):
        self.transform = T.Compose([
            T.Resize((224, 224)),
            T.ToTensor(),
            T.Normalize(mean=[0.4, 0.4, 0.4], std=[0.2, 0.2, 0.2])
        ])

        self.resnet_session = onnxruntime.InferenceSession(
            "./cls/model/resnet18.onnx")

    def infer(self, img):
        class_names = ['airport', 'building', 'forest', 'other', 'overpass',
                       'rectangular_farmland', 'sea', 'storage_tank']
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        input = self.transform(img).unsqueeze(0)

        inputs = {self.resnet_session.get_inputs()[0].name: input.numpy()}
        outs = self.resnet_session.run(None, inputs)[0]
        result = class_names[np.argmax(outs)]
        return result


if __name__ == '__main__':
    model = ResNet()
    import time
    a = time.time()
    img = cv2.imread('./data/18_21_39_2021_12_14.png')
    result = model.infer(img)
    b = time.time()
    print('waste time', b-a)
    print(result)
