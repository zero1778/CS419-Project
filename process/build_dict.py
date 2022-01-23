import os, cv2
from model.model import Model
from tqdm import tqdm
import torch, pickle


def main():
    collection_path = "../../data/oxbuild_images/"
    collection_vector_path = "./collection_vector/"
    imgs = sorted(os.listdir(collection_path))
    result = []
    model = Model(1)
    for each in tqdm(imgs):
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
 
    with open(collection_vector_path + 'model1_vec.pickle', 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()