import cv2
import numpy as np

square_size = 2.2       # One side length of a chessboard square [cm]
pattern_size = (7, 7)   # Number of intersection points
reference_img = 20      # The number of reference images

# Specify the chessboard coordinates (X,Y,0)
pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
pattern_points *= square_size
objpoints = []
imgpoints = []

# Capture images from camera
capture = cv2.VideoCapture(0)

while len(objpoints) < reference_img:
    ret, img = capture.read()
    height = img.shape[0]
    width = img.shape[1]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecting chessboard corners
    ret, corner = cv2.findChessboardCorners(gray, pattern_size)
    # If found, add object points, image points and draw chessboard corners
    if ret == True:
        print("Detect Chess Board Coners")
        print(str(len(objpoints)+1) + "/" + str(reference_img))
        term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
        corners = cv2.cornerSubPix(gray, corner, (5,5), (-1,-1), term)
        imgpoints.append(corner.reshape(-1, 2))
        objpoints.append(pattern_points)
        img = cv2.drawChessboardCorners(img, (7,6), corners,ret)
        ###  Draw chessboard corners using drawChessboardCorners  ###

    cv2.imshow('image', img)

    if cv2.waitKey(200) & 0xFF == ord('q'):
        break

print("Calculating camera parameter...")
err, mtx, dist, f_x,f_y= cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
###  Calculate internal camera parameters & store error and the camera matrix to err and mtx, respectively  ###
aspect_ratio=np.array(f_y)/np.array(f_x)
###  Calculate aspect ratio by f_y/f_x  ###

print("RMS = ", err)
print(mtx)
print("Aspect Ratio = ", aspect_ratio)