import cv2
import numpy as np
import os

drawing = False         # true if mouse is pressed
g_color = (0, 0, 255)   # paint color
g_size = 5              # pen size
ix, iy = -1, -1

color_pallet = {ord('r'): (0, 0, 255), ord('g'): (0, 255, 0), ord('b'): (255, 0, 0),
                ord('c'): (233, 160, 0), ord('m'): (127, 0, 228), ord('y'): (0, 220, 255),
                ord('w'): (255, 255, 255), ord('B'): (0, 0, 0)}
pen_size = {ord('1'): 1, ord('2'): 2, ord('3'): 3,
            ord('4'): 4, ord('5'): 5, ord('6'): 6,
            ord('7'): 7, ord('8'): 8, ord('9'): 9}

# mouse callback function
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img, (x, y), g_size, g_color, -1) ### Draw circle using cv2.circle function where g_size is radius and g_color is color ###

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img, (x,y), g_size, g_color, -1) ### Draw circle using cv2.circle function where g_size is radius and g_color is color ###


img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('PaintTool')
cv2.setMouseCallback('PaintTool', draw_circle)

while(1):
    cv2.imshow('PaintTool', img)
    k = cv2.waitKey(1) & 0xFF
    if (k==ord("r") or k==ord("g") or k==ord("b") or k==ord("c") or k==ord("m") or k==ord("y") or k==ord("w") or k==ord("B")): ### IF statement to determine if k is a key for color_pallet ###
        g_color = color_pallet[k]
    if (k==ord("1") or k==ord("2") or k==ord("3") or k==ord("4") or k==ord("5") or k==ord("6") or k==ord("7") or k==ord("8") or k==ord("9")): ### ELSE IF statement to determine if k is a key for pen_size ###
        g_size = pen_size[k]        
    elif k == ord('q'):
        cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/13-2_result.bmp", img)
        break
    elif k == 27:
        break

cv2.destroyAllWindows()