import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi, sqrt

n = 100
x = np.linspace(0, 2*pi, n)
y = np.linspace(0, 2*pi, n)
X, Y = np.meshgrid(x, y)
Z = sin(X)*sin(Y)

plt.pcolormesh(X, Y, Z, cmap='RdBu')

cont=plt.contour(X,Y,Z,  10, Vmax=0.5, camp='summer')

plt.show()
