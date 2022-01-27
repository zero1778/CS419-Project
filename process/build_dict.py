import os, cv2
from model.model import Model
from tqdm import tqdm
import torch, pickle


def main():
    collection_path = "../data/oxbuild_images/"
    collection_vector_path = "./collection_vector/"
    imgs = sorted(os.listdir(collection_path))

    image_collection = [imgs[x:x+900] for x in range(0, len(imgs), 900)]
    
    model = Model(1)    

    i = 1
    for chuck in image_collection:
        result = []
        for each in tqdm(chuck):
            img_path = collection_path + each
            img = cv2.imread(img_path) 
            img = cv2.resize(img, (224, 224))
            img = img.transpose((2, 0, 1))
            img = img.reshape((1, 3, 224, 224))
            img = torch.from_numpy(img)
            img = img.float()
            output = model.predict(img).reshape(-1)
            result.append(output)

        result = torch.stack(result).detach().numpy()
    
        with open(collection_vector_path + 'model1_vec_' + str(i) + '.pickle', 'wb') as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)

        i+=1
        break

if __name__ == "__main__":
    main()