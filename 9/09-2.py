import cv2
import math
import numpy as np

def color_difference(RGBcolor1, RGBcolor2):
 BGRlist = np.zeros((1, 2, 3), np.uint8)
 """ Change the order RGB to BGR and set input 2 colors to BGRlist """
 for i in range(3):
  BGRlist.itemset((0, 0, i), RGBcolor1[2-i])
  BGRlist.itemset((0, 1, i), RGBcolor2[2-i])

 Lablist = cv2.cvtColor(BGRlist, cv2.COLOR_BGR2LAB)

 Lablist2 = Lablist.astype(dtype=np.float_)## Define Lablist2 with Lablist cast in a float type ##

 Lablist2[:,:,0] = 100/255  # Return the normalized L range 
 Lablist2[:,:,1:3] -= 128  # Return the normalized a* b* ranges
 print(Lablist2)     # This is for debug

 distance=math.sqrt(((Lablist2[0][0][0]-Lablist2[0][1][0])**2)+((Lablist2[0][0][1]-Lablist2[0][1][1])**2)+((Lablist2[0][0][2]-Lablist2[0][1][2])**2))## Using Lablist2, calculate the distance between 2 colors on L*a*b* space ##

 return distance

RGB1 = [100, 10, 0]
RGB2 = [0, 10, 200]
print(color_difference(RGB1, RGB2))
RGB3 = [100, 10, 5]
RGB4 = [100, 8, 4]
print(color_difference(RGB3, RGB4))