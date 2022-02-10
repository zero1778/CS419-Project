
from json.tool import main
from re import S
import cv2, os
from process.model.model import Model
from process.model.utils import norm_mean_std
# from model import Model
import torch, pickle
# import pickle5 as pickle
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances, cosine_distances

def dotprod_dist(x, y):
    d = x.dot(y.T)
    d = (d - d.min(1)[:, np.newaxis]) / (d.max(1) - d.min(1))[:, np.newaxis]
    return 1 - d

os.environ['KMP_DUPLICATE_LIB_OK']='True'

def ret_answer(collection_path, priority_list_idx, type_model=1):
    priority_list = []

    if (type_model in [1, 3, 4, 5, 6, 7, 8]):
        imgs = sorted(os.listdir(collection_path))
        priority_list = [imgs[i][:-4] for i in priority_list_idx]
        # import pdb; pdb.set_trace()
    elif (type_model == 2):
        imgs = sorted(os.listdir(collection_path))
        gt_path = "data/gt_files_170407/"

        # list_collection = os.listdir(gt_path)
        list_collection = list(sorted(set([each.replace("_" + each.split("_")[-1], "") for each in os.listdir(gt_path) ])))
        # pre_priority_list = [imgs[i] for i in priority_list_idx[:2]]
        
        # def get_collection():

        for idx in priority_list_idx[:2]:
            f = open(gt_path + list_collection[idx] + "_good.txt", "r")
            lines = f.read().splitlines()
            priority_list += lines

            f = open(gt_path + list_collection[idx] + "_ok.txt", "r")
            lines = f.read().splitlines()
            priority_list += lines
        priority_list = list(dict.fromkeys(priority_list))
    return priority_list

model = None
collection_vec = []
collection_path = 0
type_model_ = 1

def dist_func(mode):
    factory = {
        1: euclidean_distances,
        2: cosine_distances,
        3: dotprod_dist,
    }
    if mode in factory:
        return factory[mode]
    else:
        raise Exception('Invalid mode.')

def initialize (type_model=1):
    global model, collection_path, collection_vec, type_model_
    type_model_ = type_model
    collection_path = "data/oxbuild_images/"
    collection_vector_path = "process/collection_vector/model" + str(type_model) + "_vec.pickle"
    if (type_model == 1):
        collection_vector_path = "process/collection_vector/model" + str(type_model) + "_vec.pickle"
    elif (type_model == 3):
        collection_vector_path = "process/collection_vector/model_resnet18_noval_vec.pickle"
    elif (type_model == 2):
        collection_path = "data/oxbuild_images_crop/"
    elif (type_model == 6):
        collection_vector_path = "process/collection_vector/model_resnet50_noval_vec.pickle"
    elif (type_model == 7):
        collection_vector_path = "process/collection_vector/model_b0_noval_vec.pickle"
    elif (type_model == 8):
        collection_vector_path = "process/collection_vector/model_resnet50_noval_vec.pickle"
        collection_vector_path1 = "process/collection_vector/model_b0_noval_vec.pickle"
    elif (type_model == 9):
        collection_vector_path = "process/collection_vector/model_att_noval_vec.pickle"

    if (type_model in [1,2,3,6,7,9]):
        with open(collection_vector_path, 'rb') as handle:
            collection_vec.append(pickle.load(handle))
        model = Model(type_model)
    elif (type_model == 8):
        with open(collection_vector_path, 'rb') as handle:
            collection_vec.append(pickle.load(handle))
        with open(collection_vector_path1, 'rb') as handle:
            collection_vec.append(pickle.load(handle))
        model = Model(type_model)
    elif type_model == 4:
        with open(collection_vector_path, 'rb') as f:
            sift_descs = pickle.load(f)
        model = Model(type_model, sift_descs=sift_descs, matcher_type='bf')
    elif type_model == 5:
        with open(collection_vector_path, 'rb') as f:
            orb_descs = pickle.load(f)
        model = Model(type_model, orb_descs=orb_descs)

# img of type PIL.Image
def  process(img, eval_method = 1, topK=20):
    """
        img: numpy array
        eval_method: 1: cosine, 2: euclidean, 3: dot product
    """
    global type_model_, model, collection_vec, collection_path
    type_model = type_model_
    priority_list = []
    # if (img.shape[-1] > 3):
    #     img = img[:, :, :3]
    # elif (img.shape[2] == None):
    #     img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    if (type_model in [1,2,3,6,7,9]):
        img = norm_mean_std(img)
        output = model.predict(img).reshape(-1).reshape(1, -1).detach().numpy()
        
        dist = dist_func(eval_method)
        dist_mat = dist(output, collection_vec[0]).reshape(-1)
        priority_list_idx = dist_mat.argsort()[:topK]
        
    elif type_model in [4, 5]:
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        priority_list_idx = model.predict(img)[:topK]
    elif type_model == 8:
        alpha = 0.5
        img = norm_mean_std(img)
        output1 = model.predict(img, num = 2).reshape(-1).reshape(1, -1).detach().numpy()
        output2 = model.predict(img, num = 3).reshape(-1).reshape(1, -1).detach().numpy()
        
        dist = dist_func(eval_method)
        dist_mat1 = dist(output1, collection_vec[0]).reshape(-1)
        dist_mat2 = dist(output2, collection_vec[1]).reshape(-1)
        dist_mat = dist_mat1*alpha + dist_mat2*(1 - alpha)

        priority_list_idx = dist_mat.argsort()[:topK]
    priority_list = ret_answer(collection_path, priority_list_idx, type_model)
    return priority_list


if __name__ == '__main__':
    print(process(cv2.imread("data/oxbuild_images_crop/01_all_souls_000013.jpg")))
