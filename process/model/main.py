
from json.tool import main
from re import S
import cv2, os
from process.model.model import Model
from process.model.utils import norm_mean_std
# from model import Model
import torch, pickle
# import pickle5 as pickle
import numpy as np

os.environ['KMP_DUPLICATE_LIB_OK']='True'


def cos_sim_2d(x, y):
    norm_x = x / np.linalg.norm(x, axis=1, keepdims=True)
    norm_y = y / np.linalg.norm(y, axis=1, keepdims=True)
    return np.matmul(norm_x, norm_y.T)

def ret_answer(collection_path, priority_list_idx, type_model=1):
    priority_list = []

    if (type_model == 1):
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

def process(img, type_model=1, topK=20):
    collection_vector_path = "process/collection_vector/model" + str(type_model) + "_vec.pickle"
    if (type_model == 1 or type_model == 3):
        collection_path = "data/oxbuild_images/"
    elif (type_model == 2):
        collection_path = "data/oxbuild_images_crop/"

    with open(collection_vector_path, 'rb') as handle:
        collection_vec = pickle.load(handle)
        
    model = Model(type_model)

    if (img.shape[-1] > 3):
        img = img[:, :, :3]
    elif (img.shape[2] == None):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    img = cv2.resize(img, (224, 224))       
    img = norm_mean_std(img)
    img = torch.from_numpy(img)
    output = model.predict(img).reshape(-1).reshape(1, -1).detach().numpy()

    cosine_similarity = cos_sim_2d(output, collection_vec).reshape(-1)
    priority_list_idx = cosine_similarity.argsort()[-topK:][::-1]
    # import pdb; pdb.set_trace()
    priority_list = ret_answer(collection_path, priority_list_idx, type_model)
    return priority_list


if __name__ == '__main__':
    print(process(cv2.imread("data/oxbuild_images_crop/01_all_souls_000013.jpg")))