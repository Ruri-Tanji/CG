import cv2
import os
import numpy as np

def drawOptFlow(img, gray, flow, step=16, dispsc=10):
    cimg    = img.copy()
    h, w = img.shape[:2] ###  Get the height h and width w from img  ###
    y, x    = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    dx, dy  = flow[y,x].T * dispsc

    dist = np.sqrt((dx)**2 + (dy)**2) ###  Calculate a length of optical flow vector and store it to dist  ###

    idx     = np.where(3 < dist)
    x, y    = x[idx], y[idx]
    dx, dy  = dx[idx], dy[idx]
    lines = np.vstack([x, y, x+dx, y+dy]).T.reshape(-1, 2, 2)
    lines = lines.astype(np.int32)

    cv2.polylines(cimg, lines, False, (0, 0, 255), 1)
    return cimg

frame1 = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/billiards04.bmp", cv2.IMREAD_COLOR)
frame2 = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/billiards05.bmp", cv2.IMREAD_COLOR)
prev_frame = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
next_frame = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

flow = cv2.calcOpticalFlowFarneback(prev_frame, next_frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
rgb2=drawOptFlow(frame1, frame2, flow, 10, 10) ###  Call drawOptFlow in specifying step=10 and substitute the results into rgb2  ###

cv2.imshow('frame2',rgb2)
k = cv2.waitKey(0)
if k == ord('q'):
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/opticalhsv.png",rgb2)