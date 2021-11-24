import cv2
import numpy as np
import os
import svgwrite

# load image, change color spaces, and smoothing
img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/INIAD_logo.png")
im=cv2.resize(img,(10000,10000))

im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
retval, im_bw = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 輪郭の検出
contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# 全ての輪郭を書き込んで出力
#im_con = im.copy()
#cv2.drawContours(im_con, contours, -1, (0,255,0), 2)

# 輪郭直線近似
approx = []
for i in range(len(contours)):
    cnt = contours[i]
    epsilon = 0.0001*cv2.arcLength(cnt,True)
    a = len(cv2.approxPolyDP(cnt,epsilon,True))
    for j in range(a):
        x = cv2.approxPolyDP(cnt,epsilon,True)[j][0][0]*0.01
        y = cv2.approxPolyDP(cnt,epsilon,True)[j][0][1]*0.01
        #print(x)
        approx.append([x, y])
    #print(cv2.approxPolyDP(cnt,epsilon,True))
    #approx.append(cv2.approxPolyDP(cnt,epsilon,True))

#print(approx)

img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/INIAD_logo.png")
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_HSV = cv2.GaussianBlur(img_HSV, (9, 9), 3)

# detect
img_H, img_S, img_V = cv2.split(img_HSV)

ret,img_1 = cv2.threshold(img_H, 50, 255, cv2.THRESH_BINARY)
cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/iniad1.bmp", img_1)

# load image, change color spaces, and smoothing
img1 = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/iniad1.bmp")
im=cv2.resize(img1,(10000,10000))
im1 = cv2.bitwise_not(im)
im_gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
retval, im_bw = cv2.threshold(im_gray1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 輪郭の検出
contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# 輪郭直線近似
approx1 = []
for i in range(len(contours)):
    cnt = contours[i]
    epsilon = 0.0001*cv2.arcLength(cnt,True)
    a = len(cv2.approxPolyDP(cnt,epsilon,True))
    for j in range(a):
        x = cv2.approxPolyDP(cnt,epsilon,True)[j][0][0]*0.01
        y = cv2.approxPolyDP(cnt,epsilon,True)[j][0][1]*0.01
        approx1.append([x, y])

color = "skyblue"
dwg = svgwrite.Drawing(os.path.dirname(os.path.abspath(__file__))+"/INIAD_logo.svg")
dwg.add( dwg.polygon( points=approx ) )
dwg.add( dwg.polygon( points=approx1, fill=color ) )
dwg.save()