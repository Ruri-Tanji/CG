import cv2
import numpy as np
import os

def k_means(src, K):
    Z=src.reshape((-1, 3))
    Z=np.float32(Z)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 15, 1.0)

    ret, label, center = cv2.kmeans(Z, K, None, criteria, 15, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)

    res = center[label.flatten()]
    result_image = res.reshape((src.shape))
    return result_image

def canny(src):
    threshold1 = 220
    threshold2 = 300
    edge_img = cv2.Canny(src, threshold1, threshold2)
    image = cv2.bitwise_not(edge_img)
    return image

img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/Mandrill.bmp", cv2.COLOR_BGR2RGB)

k_means = k_means(img, 15)
canny = canny(img)

#cv2.imshow('Input_image',img)
#cv2.imshow('k_means',k_means)
#cv2.imshow('canny',canny)

h,w = k_means.shape[:2]
canny = cv2.resize(canny,(w,h))
canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR) 
result = cv2.bitwise_and(k_means, canny)
cv2.imshow('result',result)

k = cv2.waitKey(0)
if k == ord('q'):
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/opticalhsv.png",rgb2)