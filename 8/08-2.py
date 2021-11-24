from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import copy
import math
import sys

win_x = 400
win_y = 400
NX = 100
NY = 100
temp = [[273.0 for j in range(NY+2)] for i in range(NX+2)]
step = 0
color_map = [[0]*3]*256
g_k = 0.002
dt = 0.01


def update_Temperature(T, k, dt, dx, dy):
    tp = T.copy()
    Xsize = len(T)
    Ysize = len(T[0])

    for i in range(1, Xsize-2):
        for j in range(1, Ysize-2):
            T[i][j] = tp[i][j] + k * (((tp[i+1][j] - 2*tp[i][j] + T[i-1][j]) / (dx)**2) + ((tp[i][j+1] - 2*tp[i][j] + tp[i][j-1]) / (dy)**2)) * dt ## calculate the temperature T[i][j] using tp, k, dt, dx and dy ##

    for i in range(0, Xsize):
        T[i][0] = 273.0
        T[i][Ysize-1] = 273.0
    for j in range(0, Ysize):
        T[0][j] = 273.0
        T[Xsize-1][j] = 273.0

    return T


def calcColorMap():
    global color_map
    for i in range(256):
        r = 1.0
        g = 0.0
        b = 0.0
        if i <= 255:
            r = 1.0
            g = 4.0 - 4.0 * i / 255.0
            b = 0
        if i <= 191:
            r = 4.0 * i / 255.0 - 2.0
            g = 1.0
            b = 0
        if i <= 127:
            r = 0.0
            g = 1.0
            b = 2.0 - 4.0 * i / 255.0
        if i <= 63:
            r = 0.0
            g = 4.0 * i / 255.0
            b = 1.0
        color_map[i] = [r, g, b]


def draw_2D_ScalarField(sf, min, max):
    dx = 1.0/NX
    dy = 1.0/NY
    glBegin(GL_QUADS)
    for i in range(0, NX):
        x = i/NX
        for j in range(0, NY):
            y = j/NY
            index00 = int(255 * (sf[i][j] - min)/(max - min)) if sf[i][j] < max else 255
            glColor3f(color_map[index00][0], color_map[index00][1], color_map[index00][2])
            glVertex2f(x, y)

            index10 = int(255 * (sf[i+1][j] - min)/(max - min)) if sf[i+1][j] < max else 255
            glColor3f(color_map[index10][0], color_map[index10][1], color_map[index10][2])
            glVertex2f(x + dx, y)

            index11 = int(255 * (sf[i+1][j+1] - min)/(max - min)) if sf[i+1][j+1] < max else 255
            glColor3f(color_map[index11][0], color_map[index11][1], color_map[index11][2])
            glVertex2f(x + dx, y + dy)

            index01 = int(255 * (sf[i][j+1] - min)/(max - min)) if sf[i][j+1] < max else 255
            glColor3f(color_map[index01][0], color_map[index01][1], color_map[index01][2])
            glVertex2f(x, y + dy)
    glEnd()


def reshape(width, height):
    global win_x, win_y
    glutReshapeWindow(width, height)
    win_x = width
    win_y = height
    glViewport(0, 0, win_x, win_y)


def idle():
    global step, temp
    step += 1
    temp = update_Temperature(temp, g_k, dt, 1.0/NX, 1.0/NY) ## update the temperature field ##
    """ Place the heat source for up to 1 second """
    if step*dt < 1:
        for i in range(int(NX/2-4), int(NX/2+4)):
            for j in range(int(NY/2-4), int(NY/2+4)):
                temp[i][j] = 373.0
    if step % 100 == 0:
        print("STEP:", step)
    glutPostRedisplay()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(win_x, win_y)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Heat conduction")
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
    """ Initial heat source placement """
    for i in range(int(NX/2-4), int(NX/2+4)):
        for j in range(int(NY/2-4), int(NY/2+4)):
            temp[i][j] = 373.0


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw a scalar field
    draw_2D_ScalarField(temp, 273, 373)

    glFlush()
    glutSwapBuffers()


if __name__ == "__main__":
    calcColorMap()
    main()
