import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi, sqrt

n = 100
x = np.linspace(0, 2*pi, n)
y = np.linspace(0, 2*pi, n)
X, Y = np.meshgrid(x, y)

# (u, v) = \nabla -cos(X)*cos(Y)    Pre-calculate u and v manually.
u = sin(X)*cos(Y) ###  Calculate u  ###
v = cos(X)*sin(Y) ###  Calculate v  ###
speed = sqrt(u**2 + v**2) ###  Calculate speed from u and v  ###

# Plot
strm = plt.streamplot(X, Y, u, v, color=speed, linewidth = 0.8, cmap='hsv')
plt.colorbar(strm.lines)
plt.show()