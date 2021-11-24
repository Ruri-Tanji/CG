import cv2
import numpy as np
import os

def equalize_hist(src):
    imax = src.max()
    imin = src.min()
    imean = src.mean()
    ivar = src.var()
    imedian = np.median(src)
    unique, freq = np.unique(src, return_counts=True)
    imode = unique[np.argmax(freq)]

    print(f'max:{imax}',f'min:{imin}',f'mean:{imean}',f'var:{ivar}',f'median:{imedian}',f'mode:{imode}', sep='\n')


img = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/"+"Cameraman.bmp", cv2.IMREAD_GRAYSCALE)

dst = equalize_hist(img)