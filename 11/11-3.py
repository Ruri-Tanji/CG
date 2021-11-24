import cv2
import os
import numpy as np
img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/salt_pepper.png", 0)

kernal = np.ones((5,5),np.uint8)
closing = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernal)
opening = cv2.morphologyEx(closing,cv2.MORPH_OPEN,kernal)
opening1=cv2.resize(opening,(300,300))

cv2.imshow("output", opening1)


k = cv2.waitKey(0)
if k == ord('q'):    
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/output.bmp", opening1)
    cv2.destroyAllWindows()