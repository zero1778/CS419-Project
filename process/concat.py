import os
import numpy as np
import pickle5 as pickle 
collection_vector_path = "./process/collection_vector/model3/"

files = sorted(os.listdir(collection_vector_path))
res = np.zeros((1, 1000))
for each in files:
    with open(collection_vector_path + each, 'rb') as handle:
        f = pickle.load(handle)
        # import pdb; pdb.set_trace()
        res = np.concatenate((res, f), axis = 0)

res = res[1:, :]
import pdb; pdb.set_trace()

with open(collection_vector_path + "../model3_vec.pickle", 'wb') as handle:
    pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)