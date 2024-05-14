import os
import numpy as np
import cv2
from PIL.Image import open, fromarray, Image
from Pixel_Correlation import correlation_general

def main(path: str, iterations: int, ACMMatrix: np.ndarray, keep_all: bool = False, encrypt: bool = False, name: str = "ACM-{name}-{index}.png") -> tuple[Image, int, float] | Image:
    
    title : str = os.path.splitext(os.path.split(path)[1])[0]
    counter : int = 0
    min_iter : int = 0
    min_correlation : float = 1

    with open(path) as image:
 
        _, size, n_channels = np.array(image).shape
        current_image : np.ndarray = np.array(image).copy()
        print(np.amin(current_image), np.amax(current_image))
    
        x_image, y_image = np.meshgrid(np.arange(size), np.arange(size))

        nx_image, ny_image = np.dot(ACMMatrix, [x_image.flatten(), y_image.flatten()]) % size
        nx_image, ny_image = nx_image.reshape(x_image.shape), ny_image.reshape(y_image.shape)

        transformed_image : np.ndarray = np.zeros((size, size, n_channels)).astype(np.uint8)
        ny_image = size - ny_image - 1
        y_image = size - y_image - 1

        while counter < iterations:
            transformed_image[ny_image, nx_image] = current_image[y_image, x_image]

            if counter > 0 and not keep_all:
                os.remove("Results/" + path)

            counter += 1
            path = name.format(name = title, index = counter)
            cv2.imwrite("Results/" + path, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))
            current_image = transformed_image.copy()

            if encrypt == True:
                current_correlation = correlation_general(current_image)
                if current_correlation < min_correlation:
                    min_correlation = current_correlation
                    min_iter = counter
        print(np.amin(current_image), np.amax(current_image))
        image = fromarray(current_image)

    return (image, min_iter, min_correlation) if encrypt == True else image

if __name__ == "__main__":

    result, it, corr = main("Dataset/317/airplane.png", 316, [[237, 255], [190, 64]], False, True)