import os, cv2
from process.model.main import process
import pandas as pd

cmd = "./evaluation/compute_ap.exe "
# cmd = ".\evaluation\compute_ap.exe "

#TODO: ảnh dùng query để trong folder này, chung parent vs data train
path = "./data/gt_files_170407/"
img_path = "./data/oxbuild_images_crop/"
rPath = "./evaluation/result/"
files = os.listdir(path)
end = len("_query.txt")
queries = [q[:-end] for q in files if q.endswith("query.txt")]


for q in queries:
    gtq = path + q 
    with open(gtq, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split(' ')
            img_name = line[0][5:]
            img_name = img_name + '.jpg'
    img = cv2.read(img_path + img_name)
    topK = process(img)
    import pdb; pdb.set_trace()
    resultPath = rPath + q + "_top.txt"
    with open(resultPath, 'w') as f:
        f.write("\n".join(topK))

    command = cmd + gtq + " " + resultPath
    os.system(command)

df = pd.read_csv('AP.txt', sep=" ")
df.columns = ["query", "AP"]
print("MAP = ", df["AP"].mean())