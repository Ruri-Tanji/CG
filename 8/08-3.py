from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import copy
import math
import sys

win_x = 400
win_y = 400

m = 0.1
g= 9.8
v = 0
y = 1.0
a = g
e = 0.9

step = 0
dt = 0.0002
t = 0
h=0

frame_no = 0

def update():
    global v, y, h

    if v < 0 :
        h = -1
    elif y <= 0.05:
        h= 1
        
        
    if h== -1:
        v = v + a * dt
        y=y - (v * dt)
    else:
        v = -(v + a * dt)*e
        y = y + (v * dt)

    
def draw_ball(x, y, r):
    glBegin(GL_POLYGON)
    dtheta = 0
    while dtheta < 2*math.pi:
        dx = r*math.cos(dtheta) + x
        dy = r*math.sin(dtheta) + y

        glVertex2f(dx, dy)

        dtheta += math.pi/30
    glEnd()


def reshape(width, height):
    global win_x, win_y
    glutReshapeWindow(width, height)
    win_x = width
    win_y = height
    glViewport(0, 0, win_x, win_y)


def idle():
    global step, y
    step += 1
    glutPostRedisplay()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(win_x, win_y)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Pendulum")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    init()
    glutIdleFunc(idle)
    glutMainLoop()

def init():
    glViewport(0, 0, win_x, win_y)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    """ gluOrtho2D(left, right, bottom, top) """
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)    # The coordinate system to draw

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0, 1, 0)
    update()
    draw_ball(0.5, y, 0.05)
    glFlush()
    glutSwapBuffers()


if __name__ == "__main__":
    main()
