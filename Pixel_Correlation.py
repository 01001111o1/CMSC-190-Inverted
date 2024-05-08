import numpy as np
from numpy.random import choice
from PIL.Image import open

indices = [ 
            [slice(None, None), slice(None, -1), slice(None, None), slice(1, None)], #Horizontal
            [slice(None, -1), slice(None, None), slice(1, None), slice(None, None)], #Vertical
            [slice(None, -1), slice(None, -1), slice(1, None), slice(1, None)]       #Diagonal
          ]

def calculate_correlation(A : np.ndarray, idx : list[slice]) -> float:
    x : np.ndarray = A[idx[0], idx[1]].flatten()
    y : np.ndarray = A[idx[2], idx[3]].flatten()
    return np.corrcoef(x, y)[0, 1]

def correlation_general(image : np.ndarray) -> float:
    return np.mean([calculate_correlation(image, indices[i]) for i in range(3)])

def correlation(path: str) -> float:
    with open(path) as image:
        image = np.array(image)
        return correlation_general(image)

def correlation_rgb(image : np.ndarray) -> list[list[float]]:
    """
    Returns: 3x3 matrix
        Horizontal  Vertical    Diagonal
    R       x           x           x

    G       x           x           x

    B       x           x           x

    Where each x is the correlation coefficient between the intersecting color and direction
    """
    R, G, B = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    result : list[list[float]] = [[calculate_correlation(color, indices[i]) for i in range(3)] for color in [R, G, B]] 
    return result
