import cv2
import os
import numpy as np
from sklearn.cluster import KMeans

r_uni = []
g_uni = []
b_uni = []

def RGB(img):
    height, width = img.shape[:2]
    
    R=0
    B=0
    G=0
    
    for i in range(width):
        for j in range(height):
            r, g, b = img[i, j]
            R += r
            G += g
            B += b
    r_uni.append(R / (R+G+B))
    g_uni.append(G / (R+G+B))
    b_uni.append(B / (R+G+B))

files = os.listdir("./Pokemon")
for i in range(len(files)):
    img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/Pokemon/"+files[i], cv2.IMREAD_COLOR)
    RGB(img)

rgb_array = np.array([r_uni, g_uni, b_uni])
rgb_array = rgb_array.T

pred = KMeans(n_clusters=3).fit_predict(rgb_array)

for k in range(3):
    print("ID：", k)
    for s in range(len(files)):
        if pred[s] == k:
            print(files[s])
    if k!=2:
        print('\n')