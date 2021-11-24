import cv2
import os
import numpy as np

src = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/LENNA.bmp", cv2.IMREAD_GRAYSCALE)  # Load an image
# define a sobel kernel
kernel_x = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])

kernel_y = np.array([[-1, -2, -1],
                     [0, 0, 0],
                     [1, 2, 1]])

sobel_x=cv2.filter2D(src,-1,kernel_x)## Calculate sobel_x using a prepared function filter2D in OpenCV and kernel_x ##
sobel_y=cv2.filter2D(src,-1,kernel_y)## Calculate sobel_y using a prepared function filter2D in OpenCV and kernel_y ##
result = sobel_x + sobel_y

cv2.imshow("result", result)

k = cv2.waitKey(0)
if k == ord('q'):     # When the Q key is pressed, it's done.
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/10-1_sobel.bmp", result)
    cv2.destroyAllWindows()