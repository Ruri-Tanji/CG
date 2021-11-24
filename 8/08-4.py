from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import copy
import math
import sys

win_x = 400
win_y = 400

g_m = 0.1
g_Gravity = 9.80665
g_l = 0.8

step = 0
dt = 0.0002
t = 0
g_theta = 0.5
theta_vel = 0
ball_x, ball_y = 0.5, 0.5

frame_no = 0

def update():
    global ball_x, ball_y, g_theta, theta_vel
    acc = - (g_Gravity * math.sin(g_theta) / g_l)
    theta_vel = theta_vel + acc * dt
    g_theta = g_theta + theta_vel * dt

    ball_x = g_l * math.sin(g_theta) + 0.5
    ball_y = 1.0 - g_l * math.cos(g_theta)

def line(x, y):
    glBegin(GL_LINES)
    glVertex2f(0.5, 1.0)
    glVertex2f(x, y)
    glEnd()
    
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
    update()
    glColor3f(1, 1, 1)
    line(ball_x, ball_y)
    glColor3f(0, 0, 1)
    draw_ball(ball_x, ball_y, 0.05)
    glFlush()
    glutSwapBuffers()


if __name__ == "__main__":
    main()
