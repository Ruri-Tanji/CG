import cv2
import os

def search_cv2_cascade(castom_cascade_path="data"):
    from os.path import splitext, basename, join, dirname, isdir, isfile
    from glob import glob

    cv2_path = dirname(str(cv2).split()[-1].strip(">").strip("'"))
    cascade_dir_path = join(cv2_path, castom_cascade_path)
    if isdir(cascade_dir_path):
        cascade_xml_path_list = join(cascade_dir_path, "*.xml")
        cascade = {splitext(basename(path))[0][12:]:path for path in glob(cascade_xml_path_list)}
        return cascade
    else:
        return False


img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/test.jpg")

# Loading the cascade identifiers
cascade_files = search_cv2_cascade()
face_cascade = cv2.CascadeClassifier(cascade_files["frontalface_default"])### Obtain the face cascade using CascadeClassifier and cascade_files registed by "frontalface_default" ###
eye_cascade = cv2.CascadeClassifier(cascade_files["eye"])

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Search a face region
face = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(60, 60))

# Surrounding the face region with a red rectangle and eye area with a green rectangle
for (x, y, w, h) in face:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 4)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)### Search for the eyes in the face region roi_gray using detectMultiScale ###
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)### Draw the green rectangles on the eyes region ###


cv2.imshow("result", img)
k = cv2.waitKey(0)
if k == ord('q'):
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/result.bmp", img)
    cv2.destroyAllWindows()