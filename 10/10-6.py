#!/usr/bin/python
'''
    OpenCV seamlessCloning : Normal vs Mixed
    Copyright 2015 by Satya Mallick <spmallick@gmail.com>
    
'''

import cv2
import os
import numpy as np

# Read images : src image will be cloned into dst
im = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/73599.jpg",cv2.IMREAD_UNCHANGED)
obj= cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/HORSE.bmp",cv2.IMREAD_GRAYSCALE)
obj1= cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/boy.jpg",255)
print(im.shape)
print(obj.shape)
print(obj1.shape)
# Create an all white mask
mask = 255 * np.ones(obj.shape, obj.dtype)
mask1 = 255 * np.ones(obj1.shape, obj1.dtype)
# The location of the center of the src in the dst
width, height, channels = im.shape
center = (int(height/2), int(width/2))
center1 = (int(height/3), int(width/3))

# Seamlessly clone src into dst and put the results in output
normal_clone = cv2.seamlessClone(obj, im, mask, center1, cv2.NORMAL_CLONE)
mixed_clone = cv2.seamlessClone(obj, im, mask, center, cv2.MIXED_CLONE)
normal_clone1 = cv2.seamlessClone(obj1, mixed_clone, mask1, center1, cv2.NORMAL_CLONE)
mixed_clone1 = cv2.seamlessClone(obj1, mixed_clone, mask1, center1, cv2.MIXED_CLONE)

# Write results
cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/10-5_1.bmp", normal_clone1)
cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/10-5_2.bmp", mixed_clone1)