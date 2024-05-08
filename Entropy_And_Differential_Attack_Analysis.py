import numpy as np
from skimage.measure import shannon_entropy
from PIL.Image import open

def split_RGB(path : str) -> tuple:

    with open(path) as image:
    	image = np.array(image)
    	return image[:, :, 0], image[:, :, 1], image[:, :, 2]

def compute_entropy(path: str) -> float: 

	channels = split_RGB(path)
	return np.mean([shannon_entropy(channels[0]),
					shannon_entropy(channels[1]),
					shannon_entropy(channels[2])])

def compute_NPCR(path1 : str, path2 : str) -> float:
	image1 : np.ndarray = np.array(open(path1))
	image2 : np.ndarray = np.array(open(path2))
	difference : int = np.count_nonzero(image1 - image2)
	NPCR : float = (difference / (np.prod(image1.shape))) * 100
	return NPCR

def compute_UACI(loc1, loc2):
    array1 = np.array(open(loc1)).astype(float)
    array2 = np.array(open(loc2)).astype(float)
    differences = np.abs(array1 - array2) / 255.0
    UACI = np.mean(differences) * 100
    return UACI

