import numpy as np
import os
import cv2
from scipy.ndimage import uniform_filter

l=255
k1=0.01
k2=0.03

win_size = 7

def compare_images(imageA, imageB, A, B):
    #μ(平均画素値)
    mean_x = uniform_filter(imageA, size=win_size)
    mean_y = uniform_filter(imageB, size=win_size)
    #σx、σy(標準偏差)
    uxx = uniform_filter(imageA*imageA ,size = win_size)
    uyy = uniform_filter(imageB *imageB, size=win_size)
    uxy = uniform_filter(imageA * imageB, size=win_size)
    
    var_x =  uxx - mean_x * mean_x
    var_y = uyy - mean_y * mean_y
    #共分散
    cov_xy = uxy - mean_x * mean_y
    #print(cov_xy)

    c1=(k1*l)**2
    c2=(k2*l)**2
    result = ((2*mean_x*mean_y + c1)*(2*cov_xy + c2)) / ((mean_x**2 + mean_y**2 + c1)*(var_x + var_y + c2))
    #print(result)
    pad = (win_size - 1) // 2 
    mssim = result[pad:255-3][pad:3+255-3].mean()
    #print(cov_xy)
    print("{0} vs {1} => {2}".format(A, B, mssim)) 

img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"Cameraman.bmp", cv2.IMREAD_GRAYSCALE).astype(np.float64)
png = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"Cameraman.png", cv2.IMREAD_GRAYSCALE).astype(np.float64)
jpg = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"Cameraman.jpg", cv2.IMREAD_GRAYSCALE).astype(np.float64)
noise = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"Cameraman_noise.bmp", cv2.IMREAD_GRAYSCALE).astype(np.float64)
lenna = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"LENNA.bmp", cv2.IMREAD_GRAYSCALE).astype(np.float64)

a1 = compare_images(img, png, "Cameraman.bmp", "Cameraman.png")
a2 = compare_images(img, jpg,  "Cameraman.bmp", "Cameraman.jpg")
a3 = compare_images(img, noise, "Cameraman.bmp", "Cameraman_noise.bmp")
a4 = compare_images(img, lenna, "Cameraman.bmp", "LENNA.bmp")