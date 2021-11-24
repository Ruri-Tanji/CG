from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import numpy as np
import math
    
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"skew")
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

def triangle():
    glBegin(GL_LINE_LOOP)
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(1, 0, 0)
    glVertex3f(1, 1, 0)
    glEnd()

def skew(p):
    y = np.array([[1,0,0],[-2,1,0],[0,0,1]])
    arr = np.empty((0,3), int)
    for i in range(3):
        v = np.dot(y, p[i])
        arr = np.append(arr, np.array([v]), axis=0)
    z = np.array([[1,0,0],[0,1,0],[-2,0,1]])
    for i in range(3):
        v = np.dot(z, p[i])
        arr = np.append(arr, np.array([v]), axis=0)
    return arr

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    s = skew([[0,0,0],[1,0,0],[1,1,0]])
  
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)
    glVertex3f(s[0,0],s[0,1],s[0,2])
    glVertex3f(s[1,0],s[1,1],s[1,2])
    glVertex3f(s[2,0],s[2,1],s[2,2])
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0, 0, 1)
    glVertex3f(s[3,0],s[3,1],s[3,2])
    glVertex3f(s[4,0],s[4,1],s[4,2])
    glVertex3f(s[5,0],s[5,1],s[5,2])
    glEnd()

    #triangle()
    
    glFlush()

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
