import os, cv2
from model.model import Model
from model.utils import norm_mean_std
from tqdm import tqdm
import torch, pickle


def main():
    collection_path = "./data/oxbuild_images/"
    collection_vector_path = "./process/collection_vector/model1/"
    imgs = sorted(os.listdir(collection_path))
    image_collection = [imgs[x:x+500] for x in range(0, len(imgs), 500)]
    # print(imgs[:10])
    # image_collection = [imgs[:]]
    
    model = Model(2)    

    i = 1
    for chuck in image_collection:
        result = []
        for each in tqdm(chuck):
            img_path = collection_path + each
            img = cv2.imread(img_path) 
            img = cv2.resize(img, (224, 224))
            img = norm_mean_std(img)
            img = torch.from_numpy(img)
            # img = img.float()s
            output = model.predict(img).reshape(-1)
            # import pdb; pdb.set_trace()
            result.append(output)

        result = torch.stack(result).detach().numpy()
    
        with open(collection_vector_path + 'model1_vec_' + str(i) + '.pickle', 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

        i+=1
        # break

if __name__ == "__main__":
    main()