import cv2
import os
import numpy as np

#low-pass
src = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/WOMAN.bmp",0)
ft = np.fft.fft2(src) # 2D FFT
ft = np.fft.fftshift(ft) # Shift the data so that the DC component is in the center

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
dst_img1 = np.uint8(dst)

#high-pass
src = cv2.imread(os.path.dirname(os.path.abspath(__file__))+"/HORSE.bmp",0)
ft = np.fft.fft2(src) # 2D FFT
ft = np.fft.fftshift(ft) # Shift the data so that the DC component is in the center

h, w = ft.shape
mask = np.zeros((h, w))
centery = w/2
R = 20
for x in range(0, h):
    for y in range(0, w):
        if (x-centery)**2+(y-centery)**2 > R**2:### If statement where the inside of the radius R is 1 ###
            mask[x, y] = 1

lowpass = ft*mask### Calculate lowpass result on frequency space using mask and Fourier transform result ###

lowpass = np.fft.ifftshift(lowpass)
dst=np.fft.ifft2(lowpass)### Calculate inverse Fourier transform of lowpass ###
dst = np.abs(dst)
dst_img2 = np.uint8(dst)

result = cv2.addWeighted(dst_img1, 0.5, dst_img2, 0.5, 0)
cv2.imshow("Hybrid", result)

k = cv2.waitKey(0)
if k == ord('q'):     # When the Q key is pressed, it's done.
    cv2.imwrite(os.path.dirname(os.path.abspath(__file__))+"/10-4.bmp", result)
    cv2.destroyAllWindows()
