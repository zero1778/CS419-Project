from xml.etree.ElementInclude import include
from torchvision import models
import torch

class Model():
    def __init__(self, type = 1):
        if type == 1:
            self.model = Model1()
        elif type == 2:
            self.model = Model2()
        
    def predict(self, img):
        return self.model.predict(img)

class Model1():
    def __init__(self):
        self.model = models.resnet50(pretrained=True)
        self.model.eval()
        
    def predict(self, img):
        return self.model(img)

class Model2():
    def __init__(self):
        self.model = models.resnet50(pretrained=True)
        self.model.eval()
        
    def predict(self, img):
        return self.model(img)