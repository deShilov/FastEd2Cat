import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import skimage as sk


def generate_image_train(path_image, path_image_train):
    
    # тензор изображения
    image = sk.io.imread(path_image)
    
    # изменить размер 
    resize_image = resize_im(image, 256, 256)
    gray = cv2.cvtColor(resize_image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=250, threshold2=250)
    
    # 
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
        
            if edges[i][j] == 0:
                edges[i][j] = 255
            else:
                edges[i][j] = 0
    
    edges_tens = np.array([[i,i,i] for i in edges.reshape(-1)]).reshape(resize_image.shape)
    
    imagin_concat = np.zeros((edges_tens.shape[0], edges_tens.shape[1]*2, edges_tens.shape[2]), dtype=np.uint8)

    # склеиваем input и ground truth
    for i in range(edges_tens.shape[0]):
        imagin_concat[i] = np.vstack([resize_image[i], edges_tens[i]])

    Image.fromarray(imagin_concat).save(path_image_train)


def resize_im(image, nh, nw):

    h, w, c = np.shape(image)

    img = Image.fromarray(image)

    img = img.resize((nw, nh), Image.BICUBIC)
    img = np.array(img, dtype=np.uint8)
    img = np.reshape(img, (nh, nw, c))
    
    return img