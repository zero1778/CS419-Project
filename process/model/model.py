from copyreg import pickle
from distutils.log import error
from xml.etree.ElementInclude import include
from torchvision import models
from efficientnet_pytorch import EfficientNet
import torch
import cv2
import os
from tqdm import tqdm

class Model():
    def __init__(self, type = 1, **params):
        if type == 1:
            self.model = Model1()
        elif type == 2:
            self.model = Model2()
        elif type == 3:
            self.model = Model3()
        elif type == 4:
            self.model = Model4(params.get('sift_descs'))
        elif type == 5:
            self.model = Model5(params.get('orb_descs'))
        
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
    
class Model4(): # SIFT + kNN matcher
    def __init__(self, sift_descs):
        self.sift = cv2.SIFT_create()
        self.sift_descs = sift_descs
        self.matcher = cv2.BFMatcher(crossCheck = True)
        # list of ~5000 np.array of shape (n, 128) where n is unspecified.

    def predict (self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.resize(gray, (224, 224))
        kp, desc = self.sift.detectAndCompute(gray, None)
        if desc is None:
            # No keypoint
            return list(range(len(self.sift_descs)))
        results = [] # (id, measurement)

        for id, train_desc in tqdm(enumerate(self.sift_descs)):
            if train_desc.shape[0] == 0:
                score = 99999999999
            else:
                matches = self.matcher.match(desc, train_desc)
                matches = sorted(matches, key=lambda x : x.distance)[:20]
                score = 0
                for match in matches:
                    score += match.distance
                if (len(matches) > 0): 
                    score /= len(matches)
                else:
                    score = 99999999999
                results.append((id, score))
        return [x[0] for x in sorted(results, key = lambda x:x[1])]

class Model5(): 
    # ORB + kNN, ORB features is much more lightweight but only **partial** scale invariant.
    def __init__(self, orb_descs):
        self.orb = cv2.ORB_create()
        self.orb_descs = orb_descs
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

    def predict (self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp, desc = self.orb.detectAndCompute(gray, None)
        results = []

        for id, train_desc in tqdm(enumerate(self.orb_descs)):
            if train_desc.shape[0] == 0:
                score = 99999999999
            else:
                matches = self.matcher.match(desc, train_desc)
                matches = sorted(matches, key=lambda x : x.distance)
                score = 0
                for match in matches:
                    score += match.distance
                if (len(matches) > 0): 
                    score /= len(matches)
                else:
                    score = 999999999999
                results.append((id, score))
        return [x[0] for x in sorted(results, key = lambda x:x[1])]
