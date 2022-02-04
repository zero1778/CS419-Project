import os, shutil
from tqdm import tqdm

data_path = "./data/oxbuild_images/"
save_img_path = "./data/oxbuild_images_imagenet/"

files = list(sorted(set([each.replace("_" + each.split("_")[-1], "") for each in os.listdir(data_path)])))

if os.path.isdir(save_img_path) == True:
    shutil.rmtree(save_img_path)
os.mkdir(save_img_path)

for each in files:
    if os.path.isdir(save_img_path + each) == True:
        shutil.rmtree(save_img_path + each)
    os.mkdir(save_img_path + each)

ori_img = sorted(os.listdir(data_path))

for img in tqdm(ori_img):
    for label in files:
        if label in img:
            shutil.copy(data_path + img, save_img_path + label)
            break