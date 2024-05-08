import numpy as np
import cv2
from copy import deepcopy
from KTM_Generation import generateKTM
from numba import jit 

board = np.zeros((9, 8))
b_rows, b_cols = board.shape
board = generateKTM(5, 7, board)

@jit(nopython = True)
def isValid(image, row, col):
    height, width = image.shape

    if(row < 0 or row >= height or col < 0 or col >= width):
        return 0
    else:
        return image[row, col]

@jit(nopython = True)
def _8NAddition(image, row, col, decrypt = False):
    res = 0

    for i in range(-1, 2):
        for j in range(-1, 2):

            if(i == 0 and j == 0): 
                continue
            
            res += isValid(image, row + i, col + j)
    
    new_pixel = image[row, col] + res if decrypt == False else image[row, col] - res

    return new_pixel % 256

def encrypt_channel(image : np.ndarray) -> np.ndarray:

    current_image = np.array(deepcopy(image))
    height, width = image.shape    
    sequence_map = np.zeros((height, width))
    tile = np.tile(board, (height // b_rows, width // b_cols))
    sequence_map[:len(tile), :len(tile[0])] = tile

    for i in range(height):
        for j in range(width):
            current_image[i, j] = _8NAddition(current_image, i, j)

    for j in range(1, b_rows * b_cols + 1):
        for i, j in np.argwhere(sequence_map == j):
            current_image[i, j] = _8NAddition(current_image, i, j)

    for i, j in np.argwhere(sequence_map == 0):
        current_image[i, j] = _8NAddition(current_image, i, j)

    return current_image

def decrypt_channel(image : np.ndarray, board = board) -> np.ndarray:

    current_image = np.array(deepcopy(image))
    current_image = cv2.flip(current_image, -1)
    height, width = image.shape    
    sequence_map = np.zeros((height, width))
    tile = np.tile(board, (height // b_rows, width // b_cols))
    sequence_map[:len(tile), :len(tile[0])] = tile
    sequence_map = cv2.flip(sequence_map, -1)

    for i, j in np.argwhere(sequence_map == 0):
        current_image[i, j] = _8NAddition(current_image, i, j, True)

    for j in range(b_rows * b_cols, 0, -1):
        for i, j in np.argwhere(sequence_map == j):
            current_image[i, j] = _8NAddition(current_image, i, j, True)

    for i in range(height):
        for j in range(width):
            current_image[i, j] = _8NAddition(current_image, i, j, True)

    current_image = cv2.flip(current_image, -1)
    return current_image

def KTM_Encrypt(image: np.ndarray, encrypt: bool = True, board = board) -> np.ndarray:

    image = np.array(image)
    current_image = np.array(deepcopy(image))

    R, G, B = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    if encrypt == True:
        Red = encrypt_channel(R)
        Green = encrypt_channel(G)
        Blue = encrypt_channel(B)
    else:
        Red = decrypt_channel(R, board)
        Green = decrypt_channel(G, board)
        Blue = decrypt_channel(B, board)            

    current_image = cv2.merge((Red, Green, Blue))

    return current_image

