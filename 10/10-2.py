import cv2
import os
import numpy as np

src = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/WOMAN.bmp",0)
ft = np.fft.fft2(src) # 2D FFT
ft = np.fft.fftshift(ft) # Shift the data so that the DC component is in the center

Pow = np.abs(ft)**2 # Calculate power spectrum
Pow = np.log10(Pow) # Please ignore the warnings of this line
Pmax = np.max(Pow)
Pow = Pow / Pmax * 255
pow_img = Pow.astype(np.uint8)
cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/LENNA_FFT.bmp", pow_img)

h, w = ft.shape
mask = np.zeros((h, w))
centery = w/2
R = 20
for x in range(0, h):
    for y in range(0, w):
        if (x-centery)**2+(y-centery)**2<R**2:### If statement where the inside of the radius R is 1 ###
            mask[x, y] = 1

lowpass = ft*mask### Calculate lowpass result on frequency space using mask and Fourier transform result ###

lowpass = np.fft.ifftshift(lowpass)
dst=np.fft.ifft2(lowpass)### Calculate inverse Fourier transform of lowpass ###
dst = np.abs(dst)
dst_img = np.uint8(dst)
cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/10-2.bmp", dst_img)