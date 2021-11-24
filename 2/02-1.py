import math
import sys

def orth2pol(x, y, z):
    r =     math.sqrt((x*x)+(y*y)+(z*z))## Calculate r from x, y, z ##
    phi =   math.acos(z/r)## Calculate phi using an inverse trigonometric function ##
    theta = math.atan(y/x)## Calculate theta using an inverse trigonometric function ##
    
    pol = [r, phi, theta]
    return pol

def main():
    print(orth2pol(1, 1, math.sqrt(2)))
    print(orth2pol(1, -1, -math.sqrt(2)))
    print(orth2pol(-math.sqrt(3), 3, -2))

if __name__ == "__main__":
    main()
