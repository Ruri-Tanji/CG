from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math

'''
sweep
p: points
N: number of divisions
'''

def Sweep(p, N):
    glBegin(GL_LINE_LOOP)
    th = math.radians(360/N)
    for t in range(0, N):
        c = np.zeros(2)
        c[0] = (p[2][0] * math.cos(th*t)) - (p[2][2] * math.sin(th*t))
        c[1] = (p[2][0] * math.sin(th*t)) + (p[2][2] * math.cos(th*t))
        glVertex3f(p[0][0], p[0][1], p[0][2])
        glVertex3f(p[1][0], p[1][1], p[1][2])
        glVertex3f(c[0], p[2][1], c[1])
    glEnd()
    
    glBegin(GL_LINE_LOOP)
    for t in range(0, N):
        c = np.zeros(2)
        c[0] = (p[2][0] * math.cos(th*t)) - (p[2][2] * math.sin(th*t))
        c[1] = (p[2][0] * math.sin(th*t)) + (p[2][2] * math.cos(th*t))
        glVertex3f(c[0], p[2][1], c[1]) 
    glEnd()

'''
Circle
p: center points
s: number of stacked
d: number of divisions
'''

def Circle(p, r, s, d):
    th = math.radians(360/d)
    p1 = p[0]+r
    y = p[1]
    for x in range(0, s):
        glBegin(GL_LINE_LOOP)
        for t in range(0, d):
            c = np.zeros(3)
            c[0] = (p1 * math.cos(th*t)) - (p[2] * math.sin(th*t))
            c[1] = y
            c[2] = (p1 * math.sin(th*t)) + (p[2] * math.cos(th*t))
            glVertex3f(c[0], c[1], c[2])
        p1 -= r/s
        y += r/s
        glEnd()

    p1 = p[0]+r
    y = p[1]
    for t in range(0, d):
        glBegin(GL_LINE_LOOP)
        c = np.zeros(3)
        c[0] = (p1 * math.cos(th*t)) - (p[2] * math.sin(th*t))
        c[1] = y
        c[2] = (p1 * math.sin(th*t)) + (p[2] * math.cos(th*t))
        glVertex3f(p[0], p[1]+r, p[2])
        glVertex3f(c[0], c[1], c[2])
        glEnd()
        
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"round gimlet")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    init(300,300)
    glutMainLoop()

def init(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 2.0, 10.0, 0.0, -1.0, 0.0, 0.0, 1.0, 0.0)
  
    p1 = np.array([[0, 0, 0], [0, 2, 0], [2, 0, 0]])
    glColor3f(1.0, 1.0, 0.0)
    Sweep(p1, 15)

    p2 = np.array([0, -4, 0])
    glColor3f(0.0, 1.0, 1.0)
    Circle(p2, 2, 4, 15)

    glFlush()

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
