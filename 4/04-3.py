from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import numpy as np


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Dragon curve")
    glutDisplayFunc(display)
    init()
    glutMainLoop()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    """ gluOrtho2D(left, right, bottom, top) """
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)    # The coordinate system to draw


'''
calcNewDragonCurvePoint
This is a function to calculate the point after rotating p2 by theta around p1.
'''
def calcNewDragonCurvePoint(theta, p1, p2):
    rotation_matrix = np.array([[math.cos(theta), -math.sin(theta)],[math.sin(theta), math.cos(theta)]])
    before_p2 = np.array([p2[0] - p1[0], p2[1] - p1[1]])
    after_p2 = ((np.dot(rotation_matrix, before_p2))*(1/math.sqrt(2)))+ p1 ## Calculate new vertex after_p2 using rotation_matrix and before_p2 ##

    new_point = [after_p2[0], after_p2[1]]
    return new_point


'''
drawDragonCurve
generation: Repeat recursively until this value becomes 0.
point1, point2: Vertices before change (End points of a line segment)
'''
def drawDragonCurve(generation, point1, point2):
    if generation == 0:
        glBegin(GL_LINES)
        glVertex2f(point1[0], point1[1])
        glVertex2f(point2[0], point2[1])
        glEnd()

    else:
        newpoint = calcNewDragonCurvePoint(math.radians(45), point1, point2)## Calculate new vertex using calcNewDragonCurvePoint as let point1 be a rotation center ##
        drawDragonCurve((generation-1), point1,newpoint)## This's a recursive program! ##
        drawDragonCurve((generation-1), point2,newpoint)
        ## Because this is a recursive program, you can understand what to write, can't you? ##


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw Dragon curve
    glColor3f(1.0, 1.0, 1.0)
    drawDragonCurve(10, [0.25, 0.5], [0.75, 0.5])   # for debug
    #drawDragonCurve(10, [0.25, 0.5], [0.75, 0.5])

    glFlush()

if __name__ == "__main__":
    main()
