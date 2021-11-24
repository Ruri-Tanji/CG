import cv2
import os
import numpy as np

src = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/input_image.png", cv2.IMREAD_GRAYSCALE)

#二値化
gray = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

n, label = cv2.connectedComponents(gray)

# ラベリング
color_src = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
height, width = gray.shape[:2]
colors = []

colors.append(np.array([0, 0, 0]))
colors.append(np.array([255, 0, 0]))
colors.append(np.array([0, 255, 0]))
colors.append(np.array([0, 0, 255]))

# 各領域に色付け
for y in range(0, height):
    for x in range(0, width):
        if label[y, x] > 0:
            color_src[y, x] = colors[label[y, x]]
        else:
            color_src[y, x] = [0, 0, 0]

#面積
label1 = cv2.connectedComponentsWithStats(gray)

data = np.delete(label1[2], 0, 0)
center = np.delete(label1[3], 0, 0)

for i in range(3):
    x0 = data[i][0]
    y1 = data[i][1] + data[i][3]
    if i==0:
        cv2.putText(color_src, " " +str(data[i][4]), (x0, y1+20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
    elif i==1:
        cv2.putText(color_src, " " +str(data[i][4]), (x0, y1+20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
    else:
        cv2.putText(color_src, " " +str(data[i][4]), (x0, y1+20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

cv2.imshow("output", color_src)

k = cv2.waitKey(0)
if k == ord('q'):
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/11-4_output.bmp", color_src)
    cv2.destroyAllWindows()