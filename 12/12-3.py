import cv2
import numpy as np
import os
from IPython.display import Image, display
from matplotlib import pyplot as plt


def imshow(img):
    """ndarray 配列をインラインで Notebook 上に表示する。
    """
    ret, encoded = cv2.imencode(".jpg", img)
    display(Image(encoded))

# 画像を読み込む。
img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/coin_illust.png")

# グレースケールに変換する。
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny 法で2値化する。
edges = cv2.Canny(gray, 220, 300, L2gradient=True)
#cv2.imshow("result1",edges)
##cv2.imshow("result",edges)
k = cv2.waitKey(0)

def draw_line(img, theta, rho):
    h, w = img.shape[:2]
    if np.isclose(np.sin(theta), 0):
        x1, y1 = rho, 0
        x2, y2 = rho, h
    else:
        calc_y = lambda x: rho / np.sin(theta) - x * np.cos(theta) / np.sin(theta)
        x1, y1 = 0, calc_y(0)
        x2, y2 = w, calc_y(w)

    # float -> int
    x1, y1, x2, y2 = list(map(int, [x1, y1, x2, y2]))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

# 直線を描画する。
if lines is not None:
    for rho, theta in lines.squeeze(axis=1):
        draw_line(img, theta, rho)

cv2.imshow("result_",img)
k = cv2.waitKey(0)