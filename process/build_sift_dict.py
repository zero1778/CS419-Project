import os
import cv2
from tqdm import tqdm
import pickle
import numpy as np

def main():
    collection_path = "./data/oxbuild_images/"
    collection_vector_path = "./process/collection_vector/"

    imgs = sorted(os.listdir(collection_path))
    sift = cv2.SIFT_create()
    result = []
    chunk_count = 0
    cur_chunk_id = 0

    def dump_to_file (result, chunk_id):
        path = os.path.join(collection_vector_path,'model4_vec' + '.pickle')
        # print('Partial save',chunk_id,path)
        with open(path, 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

    for img_name in tqdm(imgs):
        img = cv2.imread(os.path.join(collection_path, img_name))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray,(0,0),fx=0.25,fy=0.25,interpolation=cv2.INTER_AREA)
        kp, desc = sift.detectAndCompute(gray, None)
        if (len(kp)==0):
            desc = np.empty((0, 128))
        # print('Entry descriptor.shape: ',img_name,desc.shape)
        result.append(desc)
        chunk_count += 1
        if chunk_count == 9999999:
            cur_chunk_id += 1
            dump_to_file(result, cur_chunk_id)
            chunk_count = 0
            result = []
    if chunk_count > 0:
        cur_chunk_id += 1
        dump_to_file(result, cur_chunk_id)

if __name__ == "__main__":
    main()