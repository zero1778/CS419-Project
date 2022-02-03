from xml.etree.ElementInclude import include
from torchvision import models
from efficientnet_pytorch import EfficientNet
import torch

class Model():
    def __init__(self, type = 1):
        if type == 1:
            self.model = Model1()
        elif type == 2:
            self.model = Model2()
        elif type == 3:
            self.model = Model3()
        
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
        self.feature_extractor = torch.nn.Sequential(*list(self.model.children())[:-1])
        
        
    def predict(self, img):
        return self.feature_extractor(img)

class Model3():
    def __init__(self):
        self.model = EfficientNet.from_name('efficientnet-b0')
        self.model.eval()
        checkpoint = torch.load("process/misc/model3/weight/efficientb0/model_best.pth.tar", map_location=torch.device('cpu') )
        self.model.load_state_dict(checkpoint['state_dict'])
        
        
    def predict(self, img):
        tmp = self.model(img)
        # import pdb; pdb.set_trace()
        return tmp

        