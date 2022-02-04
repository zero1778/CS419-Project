import numpy as np 

def norm_mean_std(img):
    
    img = img / 255
    img = img.astype('float32')
    
    mean = np.mean(img, axis=(0, 1, 2))  # Per channel mean
    std = np.std(img, axis=(0, 1, 2))
    img = (img - mean) / std
    img = img.transpose((2, 0, 1))
    img = img.reshape((1, 3, 224, 224))
    
    return img