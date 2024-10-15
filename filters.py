import cv2
import numpy as np

def reduce_noise(image_path):
    image = cv2.imread(image_path)
    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    return denoised_image

def reduce_gaussian(image_path):
    image = cv2.imread(image_path)
    denoised_image = cv2.GaussianBlur(image, (5, 5), 0)
    return denoised_image

def reduce_salt_and_pepper(image_path):
    image = cv2.imread(image_path)
    median = cv2.medianBlur(image, 5)
    return median

def reduce_speckle(image_path):
    image = cv2.imread(image_path)
    gaussian = cv2.GaussianBlur(image, (3, 3), 0)
    return gaussian

def reduce_poisson(image_path):
    image = cv2.imread(image_path)
    vals = len(np.unique(image))
    vals = 2 ** np.ceil(np.log2(vals))
    noisy = np.random.poisson(image * vals) / float(vals)
    return np.uint8(noisy)
