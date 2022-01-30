
from json.tool import main
import cv2, os
from process.model.model import Model
# from model import Model
import torch, pickle
# import pickle5 as pickle
import numpy as np

os.environ['KMP_DUPLICATE_LIB_OK']='True'


def cos_sim_2d(x, y):
    norm_x = x / np.linalg.norm(x, axis=1, keepdims=True)
    norm_y = y / np.linalg.norm(y, axis=1, keepdims=True)
    return np.matmul(norm_x, norm_y.T)

def process(img, topK=20):
    collection_vector_path = "process/collection_vector/model1_vec.pickle"
    collection_path = "data/oxbuild_images/"
    with open(collection_vector_path, 'rb') as handle:
        collection_vec = pickle.load(handle)
        
    model = Model(1)

    if (img.shape[-1] > 3):
        img = img[:, :, :3]
    elif (img.shape[2] == None):
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    img = cv2.resize(img, (224, 224))
    img = img.transpose((2, 0, 1))
    img = img.reshape((1, 3, 224, 224))
    img = torch.from_numpy(img)
    img = img.float()
    output = model.predict(img).reshape(-1).reshape(1, -1).detach().numpy()

    cosine_similarity = cos_sim_2d(output, collection_vec).reshape(-1)
    priority_list_idx = cosine_similarity.argsort()[-topK:][::-1]
    imgs = sorted(os.listdir(collection_path))
    priority_list = [imgs[i] for i in priority_list_idx]

    return priority_list


if __name__ == '__main__':
    print(process(""))