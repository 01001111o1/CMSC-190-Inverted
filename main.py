import os 
import numpy as np
import cv2
from KTM_Encryption import KTM_Encrypt
from ACM_Application_on_Images import ACM_Encrypt
from Entropy_And_Differential_Attack_Analysis import compute_entropy, compute_NPCR, compute_UACI
from Pixel_Correlation import correlation
from PIL.Image import fromarray, open, Image
import copy

#FILE FOR TESTING WHAT HAPPENS IF WE FIRST TO KTM BEFORE ACM

#sizes = os.listdir("Dataset/")
sizes = ['350']

ACM_Key = {'317' : (4187, [[8, 195], [215, 185]]),
		   '350' : (1200, [[313, 36], [94, 95]]),
           '316' : (1040, [[233, 129], [262, 255]]),
           '318' : (936, [[205, 203], [52, 277]]),
           '331' : (2490, [[7, 102], [232, 236]])}

ACM_Key_Modified = {'317' : (4187, [[9, 196], [215, 185]]),
		   			'350' : (1200, [[314, 36], [94, 95]]),
                    '316' : (1040, [[234, 129], [262, 255]]),
                    '318' : (936, [[206, 203], [52, 277]]),
                    '331' : (2490, [[8, 102], [232, 236]])}


iters = {'317' : [1730, 2502, 2084, 871, 3674],
		 '350' : [1003, 681, 204, 39, 917],
         '316' : [731, 338, 246, 301, 900], 
         '318' : [14, 56, 44, 39, 11],
         '331' : [1691, 2218, 449, 449, 1520]} 

new_board = [[53,  48,  43,  12,  71,  66,  41,  14],
            [44,  11,  54,  47,  42, 13,  64, 67],
            [49,  52,  45,  72,  65,  70,  15,  40],
            [10,  55,  50,  57,  46,  61,  68,  63],
            [51,  34,  37,  60,  69,  58,  39,  16],
            [36,  9,  56,  27,  38,  23,  1,   62],
            [33,  6,   35,  22,  59,  28,  17,  24],
            [8,   21,  4,   31,  26,  19,  2,   29],
            [5,   32,  7,   20,  3,   30,  25,  18]]

def cd(path: str) -> bool:
	if os.path.exists(path) and os.path.isdir(path):
		pass
	else:
		os.makedirs(path)

def encrypt(size: str, image: np.ndarray) -> np.ndarray:
    Phase1 = KTM_Encrypt(image, True)
    _, min_corr, iters = ACM_Encrypt(Phase1, *ACM_Key[size], True)
    Phase2 = ACM_Encrypt(Phase1, iters, ACM_Key[size][1])
    return Phase2, iters

def save_encrypted(size: str, path: str):

    title: str = os.path.splitext(os.path.split(path)[1])[0]
    name: str = "{name}-encrypted.png"
    image = open(path)
    encrypted, iters = encrypt(size, image)
    path: str = name.format(name = title)
    cv2.imwrite(f"Results/{size}/" + path, cv2.cvtColor(encrypted, cv2.COLOR_RGB2BGR))
    print(size, path, iters)

###################################################### NEED TO DETERMINE IF IT CAN BE CHANGED ###########################
def create_DAA(size, path: str): 
    title: str = os.path.splitext(os.path.split(path)[1])[0]
    res_path = f'Results/{size}/Differential_Attack/{title}'
    cd(res_path)
    name: str = "{name}-{type}.png"

    original = np.array(open(path))
    modified = copy.deepcopy(original)
    modified[4, 6] = 255 - modified[4, 6]
    _original_encrypted, it1 = encrypt(size, original)
    _modified_encrypted, it2 = encrypt(size, modified)

    path1 = name.format(name = title, type = 'original')
    path2 = name.format(name = title, type = 'modified')

    print(path1, it1)
    print(path2, it2)

    cv2.imwrite(res_path + "/" + path1, cv2.cvtColor(_original_encrypted, cv2.COLOR_RGB2BGR))
    cv2.imwrite(res_path + "/" + path2, cv2.cvtColor(_modified_encrypted, cv2.COLOR_RGB2BGR))

def DAA_All():
    for size in sizes:
        path = f'Dataset/{size}/'
        images = os.listdir(path)

        for image in images:
            image_path = path + image
            create_DAA(size, image_path)		

def Numerical_Results_All():
    for size in sizes:
        path = f'Results/{size}/Differential_Attack/'
        titles = os.listdir(path)

        for title in titles:
            image_path = path + title + "/"
            images = os.listdir(image_path)
            modified = image_path + images[0]
            original = image_path + images[1]
            _entropy = compute_entropy(original)
            _correlation = correlation(original)
            NPCR = compute_NPCR(modified, original)
            UACI = compute_UACI(modified, original)
            print(f'Size: {size} Title: {title} NPCR: {NPCR} UACI: {UACI} Entropy:  {_entropy}, Correlation: {_correlation}')

###################################################### NEED TO DETERMINE IF IT CAN BE CHANGED ###########################

def decrypt(iters: int, size,  path):
    title: str = os.path.splitext(os.path.split(path)[1])[0]
    title = title.split('-')[0]
    name: str = "{name}-decrypted.png"

    with open(path) as image:
        image = np.array(image)
        path = name.format(name = title)

        Phase1 = ACM_Encrypt(image, ACM_Key[size][0] - iters, ACM_Key[size][1])
        decrypted = KTM_Encrypt(Phase1, False)
        cv2.imwrite(f'Results/{size}/Decrypted/' + path, cv2.cvtColor(decrypted, cv2.COLOR_RGB2BGR))

def decrypt_modifiedkey(iters, size, path):
    title: str = os.path.splitext(os.path.split(path)[1])[0]
    title = title.split('-')[0]
    name: str = "{name}-decrypted-modified-key.png"

    with open(path) as image:
        image = np.array(image)
        path = name.format(name = title)
        
        Phase1 = KTM_Encrypt(image, False, new_board)
        decrypted = ACM_Encrypt(Phase1, ACM_Key_Modified[size][0] - iters, ACM_Key_Modified[size][1])
        cv2.imwrite(f'Results/{size}/ModifiedKey/' + path, cv2.cvtColor(decrypted, cv2.COLOR_RGB2BGR))

def decrypt_all_modifiedkey():
	for size in sizes:
		path = f'Results/{size}/'
		images = [file for file in os.listdir(path) if file.endswith(".png")]

		for index, image in enumerate(images):
			image_path = path + image
			decrypt_modifiedkey(iters[size][index], size, image_path)

def encrypt_all():
    for size in sizes:
    	path = f'Dataset/{size}/'
    	images = os.listdir(path)

    	for image in images:
    		image_path = path + image
    		save_encrypted(size, image_path)

def decrypt_all():
	for size in sizes:
		path = f'Results/{size}/'
		images = [file for file in os.listdir(path) if file.endswith(".png")]

		for index, image in enumerate(images):
			image_path = path + image
			decrypt(iters[size][index], size, image_path)

if __name__ == "__main__":
    
    #encrypt_all()
    #decrypt_all()
    #decrypt_all_modifiedkey()
    ###############################################
    #DAA_All()	
    Numerical_Results_All()
	###############################################
