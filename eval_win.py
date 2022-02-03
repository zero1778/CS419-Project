import os, cv2
from process.model.main import process
import pandas as pd
from tqdm import tqdm

cmd = "./evaluation/compute_ap.exe "
# cmd = ".\evaluation\compute_ap.exe "

#TODO: ảnh dùng query để trong folder này, chung parent vs data train
path = "./data/gt_files_170407/"
img_path = "./data/oxbuild_images_crop/"
rPath = "./evaluation/result/"
files = os.listdir(path)
end = len("_query.txt")
queries = [q[:-end] for q in files if q.endswith("query.txt")]

if os.path.isfile(rPath + "AP.txt"):
    os.remove(rPath + "AP.txt")

for q in tqdm(queries):
    gtq = path + q 
    with open(gtq + "_query.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(' ')
            img_name = line[0][5:]
            img_name = img_name + '.jpg'
    img = cv2.imread(img_path + img_name)
    topK = process(img, type_model=1, topK=2000)
    # import pdb; pdb.set_trace()
    resultPath = rPath + q + "_top.txt"
    with open(resultPath, 'w') as f:
        f.write("\n".join(topK))

    command = cmd + gtq + " " + resultPath
    os.system(command)

df = pd.read_csv(rPath + 'AP.txt', sep=" ")
df.columns = ["query", "AP"]
print("MAP = ", df["AP"].mean())