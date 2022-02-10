from copyreg import pickle
from distutils.log import error
from xml.etree.ElementInclude import include
from torchvision import models
from efficientnet_pytorch import EfficientNet
import torch
import cv2
import os
from tqdm import tqdm
import torch.nn as nn

class Model():
    def __init__(self, type = 1, **params):
        if type == 1:
            self.model = Model1()
        elif type == 2:
            self.model = Model2()
        elif type == 3:
            self.model = Model3()
        elif type == 4:
            self.model = Model4(params.get('sift_descs'), params.get('matcher_type', 'bf'))
        elif type == 5:
            self.model = Model5(params.get('orb_descs'))
        elif type == 6:
            self.model = Model6()
        elif type == 7:
            self.model = Model7()
        elif type == 8:
            self.model1 = Model6()
            self.model2 = Model7()  
        elif type == 9:
            self.model = Model9()      
            
    def predict(self, img, num=1):
        if (num == 2):
            return self.model1.predict(img)
        if (num == 3):
            return self.model2.predict(img)
        return self.model.predict(img)

class Model1():
    def __init__(self):
        self.model = models.resnet50(pretrained=True)
        self.model.eval()
        self.feature_extractor = torch.nn.Sequential(*list(self.model.children())[:-1])
        
    def predict(self, img):
        return self.feature_extractor(img)

class Model2():
    def __init__(self):
        self.model = models.resnet50(pretrained=True)
        self.model.eval()
        self.feature_extractor = torch.nn.Sequential(*list(self.model.children())[:-1])
        
    def predict(self, img):
        return self.feature_extractor(img)

class Model3():
    def __init__(self):
        self.model = models.__dict__['resnet18']()
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 17)
        self.model.eval()
        checkpoint = torch.load("process/misc/model3/weight/resnet18_noval/model_best.pth.tar", map_location=torch.device('cpu') )
        self.model.load_state_dict(checkpoint['state_dict'])
        self.feature_extractor = torch.nn.Sequential(*list(self.model.children())[:-1])

    def predict(self, img):
        return self.feature_extractor(img).reshape(1,-1)
    
class Model4(): # SIFT + kNN matcher
    def __init__(self, sift_descs, matcher_type = 'bf'):
        self.sift = cv2.SIFT_create()
        self.sift_descs = sift_descs
        self.matcher_type = matcher_type

        if self.matcher_type == 'bf':
            self.matcher = cv2.BFMatcher(crossCheck = True)
        elif self.matcher_type == 'flann':
            FLANN_INDEX_KDTREE = 1
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks=50)   # or pass empty dictionary
            self.matcher = cv2.FlannBasedMatcher(index_params,search_params)
        else:
            raise ValueError('Unknown matcher type')

    # Distance between two descriptors
    def distance (self, desc1, desc2):
        infi = 99999999999
        if desc1.shape[0] == 0 or desc2.shape[0]==0:
            return infi
        if self.matcher_type == 'flann':
            match = self.matcher.knnMatch(desc1, desc2, k=2)
            matches = []
            # Ratio test
            for (m,n) in match:
                if m.distance < 0.7 * n.distance:
                    matches.append(m)
        else:
            matches = self.matcher.match(desc1, desc2)
        matches = sorted(matches, key=lambda x : x.distance)[:20]
        score = 0
        for match in matches:
            score += match.distance
        if (len(matches) > 0): 
            score /= len(matches)
        else:
            score = infi
        return score

    def predict (self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.resize(gray, (224, 224))
        kp, desc = self.sift.detectAndCompute(gray, None)
        if desc is None:
            # No keypoint
            return list(range(len(self.sift_descs)))
        results = [] # (id, measurement)

        for id, train_desc in tqdm(enumerate(self.sift_descs)):
            score = self.distance(desc, train_desc)
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
        if desc is None:
            # No keypoint
            return list(range(len(self.orb_descs)))
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

class Model6():
    def __init__(self):
        self.model = models.__dict__['resnet50']()
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, 17)
        self.model.eval()
        checkpoint = torch.load("process/misc/model3/weight/resnet50_noval/model_best.pth.tar", map_location=torch.device('cpu') )
        self.model.load_state_dict(checkpoint['state_dict'])
        self.feature_extractor = torch.nn.Sequential(*list(self.model.children())[:-1])

    def predict(self, img):
        return self.feature_extractor(img).reshape(1,-1)


class Model7():
    def __init__(self):
        self.model = EfficientNet.from_pretrained('efficientnet-b0',num_classes=17)
        self.model.eval()
        checkpoint = torch.load("process/misc/model3/weight/efficientb0_right/model_best.pth.tar", map_location=torch.device('cpu') )
        self.model.load_state_dict(checkpoint['state_dict'])

    def predict(self, img):
        return self.model.extract_features(img).reshape(1,-1)


class Model9():
    def __init__(self):
        self.model = EfficientNet.from_pretrained('efficientnet-b1',num_classes=17)
        self.model.eval()
        checkpoint = torch.load("process/misc/model3/weight/attention/model_best.pth.tar", map_location=torch.device('cpu') )
        self.model.load_state_dict(checkpoint['state_dict'])

    def predict(self, img):
        return self.model.extract_features(img).reshape(1,-1)
