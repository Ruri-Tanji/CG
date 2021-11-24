import cv2
import os
import numpy as np

src = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/LENNA_color.bmp", cv2.IMREAD_UNCHANGED)  # Load an image
i=0
dst=src
for i in range(10):
    dst = cv2.bilateralFilter(dst,15,20,20)

    if i==0:
        cv2.imshow("Once", dst)
    if i==1:
        cv2.imshow("Twice", dst)
    i+=1
cv2.imshow("Ten Times", dst)


k = cv2.waitKey(0)
if k == ord('q'):     # When the Q key is pressed, it's done.
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/10-3.bmp", dst)
    cv2.destroyAllWindows()