import shutil, cv2, os
import torch
from process.model.model import Model
from process.model.utils import norm_mean_std
# from model import Model
import torch, pickle
import pickle5 as pickle
import torchvision.transforms as transforms
import numpy as np
from tqdm import tqdm
import PIL
from PIL import Image

from sklearn.metrics.pairwise import euclidean_distances, cosine_distances


def imshow(inp, title=None):
    """Imshow for Tensor."""
    # import pdb; pdb.set_trace()
    # inp
    inp = inp[0].numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    im = Image.fromarray((inp * 255).astype(np.uint8))
    im.save("your_file.jpeg")

def dotprod_dist(x, y):
    d = x.dot(y.T)
    d = (d - d.min(1)[:, np.newaxis]) / (d.max(1) - d.min(1))[:, np.newaxis]
    return 1 - d
def numbering(x):
    if x < 10:
        return '0' + str(x)
    return str(x)


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

ranked_list = "evaluation/result/all_souls_1_top.txt"
vis_path = "data/visualization/"
img_path = "data/oxbuild_images/"
eval_method = 2

if os.path.isdir(vis_path) == True:
    shutil.rmtree(vis_path)
os.mkdir(vis_path)

f = open(ranked_list, "r")
lines = f.read().splitlines()
f.close()

f = open("data/ranked.txt", "w")


model = Model(3)
# img = cv2.imread("data/oxbuild_images_crop/01_all_souls_000013.jpg")


img = Image.open("data/oxbuild_images_crop/01_all_souls_000013.jpg").convert('RGB')
img = norm_mean_std(img)

imshow(img)


# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# img = cv2.resize(img, (224, 224))
# img = norm_mean_std(img)
# img = torch.from_numpy(img)
vec = model.predict(img).reshape(-1).reshape(1, -1).detach().numpy()

print(111)

for idx, line in tqdm(enumerate(lines[:20])):

    img = Image.open(img_path + line + ".jpg").convert('RGB')
    img = norm_mean_std(img)

    # img = cv2.imread(img_path + line + ".jpg")
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # img = cv2.resize(img, (224, 224))
    # img = norm_mean_std(img)
    # img = torch.from_numpy(img)
    output = model.predict(img).reshape(-1).reshape(1, -1).detach().numpy()
    # import pdb; pdb.set_trace()
    dist = dist_func(eval_method)
    dist_mat = dist(output, vec).reshape(-1)
    
    f.writelines("%s\t%s\n" % (line, dist_mat[0]))
    img_name = numbering(idx + 1) + "_" + line + '.jpg'
    shutil.copy(img_path + line + ".jpg", vis_path + img_name)

f.close()
