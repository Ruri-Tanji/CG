import cv2
import os
import numpy as np

imgL = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/TSUKUBA_LEFT.png",0)
imgR = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/TSUKUBA_RIGHT.png",0)

stereo = cv2.StereoBM_create(numDisparities=32, blockSize=15)###  Stereo matching using the Block Matching method (numDisparities=32, blockSize=15)  ###
disp = stereo.compute(imgL, imgR)

result = np.uint8(np.array(disp) ) ###  Define the uint8 array result filled by zeros as same size as disp  ###
#normalizedImg= np.zeros((800, 800))
result = cv2.normalize(disp, None, np.min(disp), np.max(disp), norm_type = cv2.NORM_MINMAX,dtype = cv2.CV_8U) ###  Normalize disp image to range [min of disp, max of disp] & convert image type to uint8 using cv2.normalize function  ###

cv2.imshow("disp", result)
cv2.waitKey(0)
cv2.destroyAllWindows()