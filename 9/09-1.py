import cv2
import os
import numpy as np

src = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"Cameraman.bmp", cv2.IMREAD_GRAYSCALE)		# Load an image
#print(os.path.dirname(os.path.abspath(__file__))+"/"+"Cameraman.bmp")										# for debug
height, width = src.shape			# Get height & width of an image
result = src.copy()					# Prepare the result data with the same size as src
src_float = src.astype(np.float32)


for i in range(height):
 for j in range(width):
  result[i][j] = 255 if src_float[i][j] > 127 else 0 ## Calculate a result value at (j, i) using a ternary operator and src_float ##
  e= src_float[i][j] - result[i][j]## Calculate an error value e from a result value and a src_float value at (j, i) ##
  if j != width - 1 and j != 0 and i != height -1:
   src_float[i][j+1]  += 5*e/16## Calculate src_float value at f_1 in a slide ##
   src_float[i+1][j-1] += 3*e/16## Calculate src_float value at f_2 in a slide ##
   src_float[i+1][j] += 5*e/16## Calculate src_float value at f_3 in a slide ##
   src_float[i+1][j+1] += 3*e/16## Calculate src_float value at f_4 in a slide ##
  elif j == 0 and i != height - 1:
   src_float[i][j+1]  += 3*e/8
   src_float[i+1][j] += 3*e/8
   src_float[i+1][j+1] += e/4
  elif j == width - 1 and i != height - 1:
   src_float[i+1][j-1] += 3*e/8
   src_float[i+1][j]  += 5*e/8
  elif j != width - 1 and i == height - 1:
   src_float[i][j+1] += e


cv2.imshow("result", result) # Display the result image
cv2.imshow("src", src)    # Display the input image
 
k = cv2.waitKey(0)
if k == ord('q'):     # When the Q key is pressed, it's terminated.
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/09-1.bmp", result)
    cv2.destroyAllWindows()