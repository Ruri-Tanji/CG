from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import numpy as np
import math
import sys

win_x = 400
win_y = 400
step = 0
dt = 0.01
frame_no = 0
theta = 0


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(win_x, win_y)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"path trace animetion")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    init()
    glutIdleFunc(idle)
    glutMainLoop()

def init():
    glViewport(0, 0, win_x, win_y)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    """ gluOrtho2D(left, right, bottom, top) """
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)    # The coordinate system to draw

def display():
    global frame_no
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINE_STRIP)
    for t in np.linspace(0, math.pi*4, 1000):
        glVertex2f(0.05*t*math.cos(t) + 0.5, 0.05*t*math.sin(t) + 0.5)
    glEnd()
    #print(frame_no)

    global theta
    if theta > math.pi*4:
        theta = theta - math.pi*4
        frame_no = 0
    pos = [0.05*theta*math.cos(theta) + 0.5, 0.05*theta*math.sin(theta) + 0.5]
    next_pos = [0.05*(theta+dt)*math.cos(theta+dt) + 0.5, 0.05*(theta+dt)*math.sin(theta+dt) + 0.5]
    dir = [next_pos[0] - pos[0], next_pos[1] - pos[1]]
    drawPackman(pos, dir, step%5)
    #print(theta)

    glFlush()

    if step%5 == 0:
        frame_no += 1
    glutSwapBuffers()

def drawPackman(pos, dir, mouse):
    #print(dir)
    phi = math.atan2(dir[1], dir[0])
    if phi < 0:
        phi +=2*math.pi

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    if mouse == 0:
        glVertex2f(pos[0], pos[1])
        for i in np.linspace(phi + math.pi/6, phi - math.pi/6 + 2*math.pi, 20):
            glVertex2f(0.05*math.cos(i) + pos[0], 0.05*math.sin(i) + pos[1])
    else:
        for i in np.linspace(phi + math.pi/15, phi - math.pi/15 + 2*math.pi, 20):
            glVertex2f(0.05*math.cos(i) + pos[0], 0.05*math.sin(i) + pos[1])

    glEnd()

def reshape(width, height):
    global win_x, win_y
    glutReshapeWindow(width, height)
    win_x = width
    win_y = height
    glViewport(0, 0, win_x, win_y)


def idle():
    global step, theta
    step += 1
    theta += dt
    glutPostRedisplay()


if __name__ == "__main__":
    main()