from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math

def combination(n, r):
    return math.factorial(n) // (math.factorial(n - r) * math.factorial(r)) ## Calcurate and return combination _n C_r ##

'''
drawRationalBezier
cp: 2D control points
N: number of divisions
'''
def drawRationalBezier(cp, w, N):
    number_cp = len(cp) # number of control points
    n = number_cp - 1   # value n of n-th Bezier
    glLineWidth(3.0)
    glBegin(GL_LINE_STRIP)
    for t in np.linspace(0, 1, N):
        c = np.zeros(2) # Numerator of a Ratinal Bezier curve equation
        sum_weight = 0  # Denominator of a Ratinal Bezier curve equation
        for i in range(0, number_cp):
            c += w[i] * cp[i] * (combination(n, i) * t**i * (1-t)**(n-i)) ## Calcurate the numerator c on Bezier curve from control point cp, w and etc... ##
            sum_weight += w[i] * (combination(n, i) * t**i * (1-t)**(n-i)) ## Calcurate the denominator w on Bezier curve from weight list w and etc... ##
        glVertex2f(c[0]/sum_weight, c[1]/sum_weight) ## Specifying a vertex ##
    glEnd()

def drawLineBetweenControlPoint(cp):
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(1, 0xF0F0)
    glBegin(GL_LINE_STRIP)
    for i in range(0, len(cp)):
        glVertex2f(cp[i][0], cp[i][1])
    glEnd()
    glDisable(GL_LINE_STIPPLE)

def drawControlPoint(cp):
    glPointSize(20.0)
    glEnable(GL_POINT_SMOOTH)
    glBegin(GL_POINTS)
    for i in range(0, len(cp)):
        glVertex2f(cp[i][0], cp[i][1])
    glEnd()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Rational Bezier curve")
    glutDisplayFunc(display)
    init()
    glutMainLoop()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    """ gluOrtho2D(left, right, bottom, top) """
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)    # The coordinate system to draw

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw Bezier curve
    cp = np.array([[0.1, 0.1], [0.1, 0.9], [0.5, 0.1], [0.5, 0.9], [0.9, 0.1], [0.9, 0.9]])
    w1 = np.array([1, 1, 1, 1, 1, 1])
    w2 = np.array([1, 10, 100, 100, 10, 1])
    glColor3f(1.0, 1.0, 1.0)
    drawLineBetweenControlPoint(cp)
    glColor3f(1.0, 0.0, 0.0)
    drawRationalBezier(cp, w1, 100)
    glColor3f(0.0, 1.0, 0.0)
    drawRationalBezier(cp, w2, 200)
    glColor3f(33/255, 173/255, 229/255)
    drawControlPoint(cp)

    glFlush()

if __name__ == "__main__":
    main()
