import cv2
import os

img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/Fontana_di_Trevi.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

temp_img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/X.jpg")
temp_img = cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB)

w, h, c = temp_img.shape

res = cv2.matchTemplate(img,temp_img,cv2.TM_CCOEFF_NORMED)### Return the matching area using matchTemplate specified SSD as similarity measure and store it to res (cv2.TM_CCOEFF_NORMEDでいいのかわからない)###
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc### Return the top left coordinate to top_left ###
bottom_right = (top_left[0] + w, top_left[1] + h)### Return the bottom right coordinate to bottom_right ###
cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)

img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
cv2.imshow("Result", img)
k = cv2.waitKey(0)
if k == ord('q'):
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/12-1.bmp", img)
    cv2.destroyAllWindows()