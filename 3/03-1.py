import math
import numpy as np

def calcTriangleArea(p1, p2, p3):
    v1 = np.array(p1)
    v2 = np.array(p2)
    v3 = np.array(p3)
    cross_vector =  np.cross(v2-v1, v3-v1)   ## Calculate a cross vector using v1, v2, v3 ##
    area =  np.linalg.norm(cross_vector) / 2    ## Calculate the triangle area using cross_vector ##
    return area

def main():
    print(calcTriangleArea([2, 0, 0], [0, 2, 0], [0, 0, 2]))
    print(calcTriangleArea([0, 0, 0], [1, math.sqrt(3), 0], [-1, math.sqrt(3), 0]))

if __name__ == "__main__":
    main()
