import numpy as np
from Pixel_Correlation import correlation_general

def ACM_Encrypt(image, iterations: int, ACMMatrix: np.ndarray, compute_correlation: bool = False) -> tuple[np.ndarray, int, float] | np.ndarray:
    
    counter : int = 0
    min_iter : int = 0
    min_correlation : float = 1
 
    _, size, n_channels = np.array(image).shape
    current_image: np.ndarray = np.array(image).copy()
    x_image, y_image = np.meshgrid(np.arange(size), np.arange(size))

    nx_image, ny_image = np.dot(ACMMatrix, [x_image.flatten(), y_image.flatten()]) % size
    nx_image, ny_image = nx_image.reshape(x_image.shape), ny_image.reshape(y_image.shape)

    transformed_image : np.ndarray = np.zeros((size, size, n_channels)).astype(np.uint8)
    ny_image, y_image = size - ny_image - 1, size - y_image - 1
    
    while counter < iterations:
        transformed_image[ny_image, nx_image] = current_image[y_image, x_image]

        counter += 1            
        current_image = transformed_image.copy()

        if compute_correlation == True:
            current_correlation = correlation_general(current_image)
            if current_correlation < min_correlation:
                min_correlation = current_correlation
                min_iter = counter

    image = current_image

    return (image, min_correlation, min_iter) if compute_correlation == True else image

