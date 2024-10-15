import cv2
import numpy as np

def apply_sepia(image_path):
    image = cv2.imread(image_path)
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    sepia_image = cv2.transform(image, sepia_filter)
    sepia_image = np.clip(sepia_image, 0, 255)
    return sepia_image

def apply_bw(image_path):
    image = cv2.imread(image_path)
    bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return bw_image

def apply_vintage(image_path):
    image = cv2.imread(image_path)
    rows, cols = image.shape[:2]
    vintage_filter = np.zeros((rows, cols, 3), dtype=np.uint8)
    vintage_filter[:, :, 0] = 50
    vintage_filter[:, :, 1] = 20
    vintage_filter[:, :, 2] = 0
    vintage_image = cv2.addWeighted(image, 0.7, vintage_filter, 0.3, 0)
    return vintage_image

def apply_dramatic(image_path):
    image = cv2.imread(image_path)
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    dramatic_image = cv2.filter2D(image, -1, kernel)
    return dramatic_image
