import os
import pandas as pd

cmd = ".\compute_ap.exe "

#TODO: ảnh dùng query để trong folder này, chung parent vs data train
path = "../data/gt_files_170407/"
rPath = path
files = os.listdir(path)
end = len("_query.txt")
queries = [q[:-end] for q in files if q.endswith("query.txt")]

for q in queries:
    gtq = path + q + " "
    #TODO: nhớ chỉnh path result
    resultPath = rPath + q + "_good.txt"
    command = cmd + gtq + resultPath
    os.system(command)

df = pd.read_csv('AP.txt', sep=" ")
df.columns = ["query", "AP"]
print("MAP = ", df["AP"].mean())