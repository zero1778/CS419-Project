import numpy as np
import torchvision.transforms as transforms
import PIL
from PIL import Image
import torch

def norm_mean_std(img):
    
    # img = img / 255
    image_size = 224
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],    
                                std=[0.229, 0.224, 0.225])
    transform = transforms.Compose([
        transforms.Resize((image_size, image_size), interpolation=PIL.Image.BICUBIC),
        # transforms.Resize(image_size, interpolation=PIL.Image.BICUBIC),
        # transforms.CenterCrop(image_size),
        transforms.ToTensor(),
        normalize,
    ])
    
    # mean = [0.485, 0.456, 0.406] # Per channel mean
    # std = [0.229, 0.224, 0.225]
    # img = (img - mean) / std
    # img = img.astype('float32')

    # img = img.transpose((2, 0, 1))
    # img = img.reshape((1, 3, 224, 224))
    
    x = transform(img)
    x = x.unsqueeze(0)
    pix = np.array(x) #convert image to numpy array
    img = torch.from_numpy(pix)
    return img