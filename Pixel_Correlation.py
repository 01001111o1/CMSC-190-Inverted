import numpy as np
from numpy.random import choice
from PIL.Image import open
import matplotlib.pyplot as plt

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

def correlation_breakup(image : np.ndarray) -> list[float]:
    return [calculate_correlation(image, indices[i]) for i in range(3)]

def graph_correlation(path, num_samples = 5000, idx = indices):

    A = np.array(open(path))

    x_horizontal = A[idx[0][0], idx[0][1]].flatten()
    y_horizontal = A[idx[0][2], idx[0][3]].flatten()
    rand_index_horizontal = np.random.choice(len(x_horizontal), num_samples, replace=False)
    x_sampled_horizontal = x_horizontal[rand_index_horizontal]
    y_sampled_horizontal = y_horizontal[rand_index_horizontal]

    x_vertical = A[idx[1][0], idx[1][1]].flatten()
    y_vertical = A[idx[1][2], idx[1][3]].flatten()
    rand_index_vertical = np.random.choice(len(x_vertical), num_samples, replace=False)
    x_sampled_vertical = x_vertical[rand_index_vertical]
    y_sampled_vertical = y_vertical[rand_index_vertical]

    x_diagonal = A[idx[2][0], idx[2][1]].flatten()
    y_diagonal = A[idx[2][2], idx[2][3]].flatten()
    rand_index_diagonal = np.random.choice(len(x_diagonal), num_samples, replace=False)
    x_sampled_diagonal = x_diagonal[rand_index_diagonal]
    y_sampled_diagonal = y_diagonal[rand_index_diagonal]

    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.title('Horizontal Correlation')
    plt.scatter(x_sampled_horizontal, y_sampled_horizontal)

    plt.subplot(1, 3, 2)
    plt.title('Vertical Correlation')
    plt.scatter(x_sampled_vertical, y_sampled_vertical)

    plt.subplot(1, 3, 3)
    plt.title('Diagonal Correlation')
    plt.scatter(x_sampled_diagonal, y_sampled_diagonal)

    plt.show()

graph_correlation("Dataset/350/cow.png") #Plots of Horizontal, Vertical, and Diagonal of the original image
graph_correlation("Results/350/cow-encrypted.png") #Plots of Horizontal, and Diagonal of the encrypted image


