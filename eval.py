import os, cv2
from process.model.main import process, initialize
import pandas as pd
from tqdm import tqdm
import torchvision.transforms as transforms
from PIL import Image
import pdb

def numbering(x):
    if x < 10:
        return '0' + str(x)
    return str(x)

cmd = "./evaluation/compute_ap "
# cmd = ".\evaluation\compute_ap.exe "

# TODO: ảnh dùng query để trong folder này, chung parent vs data train
path = "./data/gt_files_170407/"
img_path = "./data/oxbuild_images_crop/"
rPath = "./evaluation/result/"
os.makedirs(rPath, exist_ok=True)
files = sorted(os.listdir(path))
end = len("_query.txt")
queries = [q[:-end] for q in files if q.endswith("query.txt")]

if os.path.isfile(rPath + "AP.txt"):
    os.remove(rPath + "AP.txt")

initialize(type_model = 6)

for idx, q in tqdm(enumerate(queries)):
    gtq = path + q 
    with open(gtq + "_query.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(' ')
            img_name = line[0][5:]
            img_name = numbering(idx + 1) + "_" + img_name + '.jpg'

    img = Image.open(img_path + img_name).convert('RGB')
    topK = process(img, eval_method=2, topK=200)
    
    resultPath = rPath + q + "_top.txt"
    with open(resultPath, 'w') as f:
        f.write("\n".join(topK))

    command = cmd + gtq + " " + resultPath
    os.system(command)

df = pd.read_csv(rPath + 'AP.txt', sep=" ")
df.columns = ["query", "AP"]
print("MAP = ", df["AP"].mean())