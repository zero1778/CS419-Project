import os, cv2
from model.model import Model
from model.utils import norm_mean_std
from tqdm import tqdm
import torch, pickle
import torchvision.transforms as transforms
import PIL
from PIL import Image
# from model.utils import norm_mean_std
def numbering(x):
    if x < 10:
        return '0' + str(x)
    return str(x)

def main():
    collection_path = "./data/oxbuild_images/"
    collection_vector_path = "./process/collection_vector/model3/resnet18_noval/"
    imgs = sorted(os.listdir(collection_path))
    # print(imgs[:10])
    # image_collection = [imgs[:]]
    image_collection = [imgs[x:min(x+1000, len(imgs))] for x in range(0, len(imgs), 1000)]
    # import pdb; pdb.set_trace()
    
    model = Model(3)    

    i = 1
    for chuck in image_collection:
        result = []
        for each in tqdm(chuck):
            img_path = collection_path + each
            img = Image.open(img_path).convert('RGB')
            img = norm_mean_std(img)
            output = model.predict(img).reshape(-1)
            # import pdb;pdb.set_trace()
            result.append(output)

        result = torch.stack(result).detach().numpy()
    
        with open(collection_vector_path + 'model3_vec_' + numbering(i) + '.pickle', 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

        i+=1
        # break

if __name__ == "__main__":
    main()