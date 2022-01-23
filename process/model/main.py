
from json.tool import main
import cv2, os
from process.model.model import Model
import torch, pickle
import numpy as np

def cos_sim_2d(x, y):
    norm_x = x / np.linalg.norm(x, axis=1, keepdims=True)
    norm_y = y / np.linalg.norm(y, axis=1, keepdims=True)
    return np.matmul(norm_x, norm_y.T)

def process(img_path):
    collection_vector_path = "process/collection_vector/model1_vec.pickle"
    collection_path = "process/data/oxbuild_images/"
    with open(collection_vector_path, 'rb') as handle:
        collection_vec = pickle.load(handle)
        
    img = cv2.imread(img_path)
    model = Model(1)

    img = cv2.resize(img, (224, 224))
    img = img.transpose((2, 0, 1))
    img = img.reshape((1, 3, 224, 224))
    img = torch.from_numpy(img)
    img = img.float()
    output = model.predict(img).reshape(-1).reshape(1, -1).detach().numpy()

    cosine_similarity = cos_sim_2d(output, collection_vec).reshape(-1)
    priority_list_idx = cosine_similarity.argsort()[(-1*collection_vec.shape[0]):][::-1]

    imgs = sorted(os.listdir(collection_path))
    priority_list = [imgs[i] for i in priority_list_idx]

    return priority_list


if __name__ == '__main__':
    print(process())