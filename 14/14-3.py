import numpy as np
import pandas as pd

A = np.array([[2, 1], [4, 1], [9, 1]], dtype=float)
b = np.array([[3], [7], [11]], dtype=float)
A_t = np.array(A).T

x = np.linalg.inv(np.dot(A_t, A))
x = np.dot(x, A_t)
x = np.dot(x, b)

print("x ≒", x[0])
print("y ≒", x[1])