import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


N = 64
size = N + 2

dt = 0.1
diff = 0.0
visc = 0.0
force = 5.0
source = 100.0
dvel = False

win_x = 512
win_y = 512

omx = 0.0
omy = 0.0
mx = 0.0
my = 0.0
mouse_down = [False, False, False]

u = np.zeros((size, size), dtype = 'float64')       # x component of velocity
u_prev = np.zeros((size, size), dtype = 'float64')
v = np.zeros((size, size), dtype = 'float64')       # y component of velocity
v_prev = np.zeros((size, size), dtype = 'float64')
dens = np.zeros((size, size), dtype = 'float64')    # density
dens_prev = np.zeros((size, size), dtype = 'float64')


def set_bnd(N, b, x):
    for i in range(1, N + 1):
        if b == 1:
            x[0, i] = -x[1, i]
        else:
            x[0, i] = x[1, i]
        if b == 1:
            x[N + 1, i] = -x[N, i]
        else:
            x[N + 1, i] = x[N, i]
        if b == 2:
            x[i, 0] = -x[i, 1]
        else:
            x[i, 0] = x[i, 1]
        if b == 2:
            x[i, N + 1] = -x[i, N]
        else:
            x[i, N + 1] = x[i, N]

    x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
    x[0, N + 1] = 0.5 * (x[1, N + 1] + x[0, N])
    x[N + 1, 0] = 0.5 * (x[N, 0] + x[N + 1, 1])
    x[N + 1, N + 1] = 0.5 * (x[N, N + 1] + x[N + 1, N])


def lin_solve(N, b, x, x0, a, c):
    for k in range(0, 10):
        x[1:N + 1, 1:N + 1] = (x0[1:N + 1, 1:N + 1] + a *
                               (x[0:N, 1:N + 1] +
                                x[2:N + 2, 1:N + 1] +
                                x[1:N + 1, 0:N] +
                                x[1:N + 1, 2:N + 2])) / c
        set_bnd(N, b, x)


def add_source(N, x, s, dt):
    size = (N + 2)
    x[0:size, 0:size] += dt * s[0:size, 0:size]


def diffuse(N, b, x, x0, diff, dt):
    a = dt * diff * N * N
    lin_solve(N, b, x, x0, a, 1 + 4 * a)


def advect(N, b, d, d0, u, v, dt):

    dt0 = dt * N
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            x = i - u[i, j]*dt0 ## calculate the location x where is backward by just dt0 according to u[i, j] ##
            y=  j - v[i, j]*dt0 ## calculate the location y where is backward by just dt0 according to v[i, j] ##
            if x < 0.5:
                x = 0.5
            if x > N + 0.5:
                x = N + 0.5
            i0 = int(x)
            i1 = i0 + 1
            if y < 0.5:
                y = 0.5
            if y > N + 0.5:
                y = N + 0.5
            j0 = int(y)
            j1 = j0 + 1
            s1 = x - i0
            s0 = 1 - s1
            t1 = y - j0
            t0 = 1 - t1
            d[i,j] = (s0 * (t0 * d0[i0, j0] + t1 * d0[i0,j1]) + s1 * (t0* d0[i1, j0] + t1 * d0[i1,j1])) ## calculate d[i, j] from surrounding d0 according to linear interpolation ##
    set_bnd(N, b, d)

def project(N, u, v, p, div):
    h = 1.0 / N
    div[1:N + 1, 1:N + 1] = (-0.5 * h *
                             (u[2:N + 2, 1:N + 1] - u[0:N, 1:N + 1] +
                              v[1:N + 1, 2:N + 2] - v[1:N + 1, 0:N]))
    p[1:N + 1, 1:N + 1] = 0
    set_bnd(N, 0, div)
    set_bnd(N, 0, p)
    lin_solve(N, 0, p, div, 1, 4)
    u[1:N + 1, 1:N + 1] -= 0.5 * (p[2:N + 2, 1:N + 1] - p[0:N, 1:N + 1]) / h
    v[1:N + 1, 1:N + 1] -= 0.5 * (p[1:N + 1, 2:N + 2] - p[1:N + 1, 0:N]) / h
    set_bnd(N, 1, u)
    set_bnd(N, 2, v)


def dens_step(N, x, x0, u, v, diff, dt):
    add_source(N, x, x0, dt)
    x0, x = x, x0  # swap
    diffuse(N, 0, x, x0, diff, dt)
    x0, x = x, x0  # swap
    advect(N, 0, x, x0, u, v, dt)


def vel_step(N, u, v, u0, v0, visc, dt):
    add_source(N, u, u0, dt)
    add_source(N, v, v0, dt)
    u0, u = u, u0  # swap
    diffuse(N, 1, u, u0, visc, dt)
    v0, v = v, v0  # swap
    diffuse(N, 2, v, v0, visc, dt)
    project(N, u, v, u0, v0)
    u0, u = u, u0  # swap
    v0, v = v, v0  # swap
    advect(N, 1, u, u0, u0, v0, dt)
    advect(N, 2, v, v0, u0, v0, dt)
    project(N, u, v, u0, v0)



def clear_data():
    global u, v, u_prev, v_prev, dens, dens_prev, size

    u[0:size, 0:size] = 0.0
    v[0:size, 0:size] = 0.0
    u_prev[0:size, 0:size] = 0.0
    v_prev[0:size, 0:size] = 0.0
    dens[0:size, 0:size] = 0.0
    dens_prev[0:size, 0:size] = 0.0


def pre_display():
    glViewport(0, 0, win_x, win_y)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)


def draw_velocity():
    h = 1.0 / N

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1.0)

    glBegin(GL_LINES)
    for i in range(1, N + 1):
        x = (i - 0.5) * h
        for j in range(1, N + 1):
            y = (j - 0.5) * h
            glColor3f(1, 0, 0)
            glVertex2f(x, y)
            glVertex2f(x + u[i, j], y + v[i, j])
    glEnd()


def draw_density():
    h = 1.0 / N

    glBegin(GL_QUADS)
    for i in range(0, N + 1):
        x = (i - 0.5) * h
        for j in range(0, N + 1):
            y = (j - 0.5) * h
            d00 = dens[i, j]
            d01 = dens[i, j + 1]
            d10 = dens[i + 1, j]
            d11 = dens[i + 1, j + 1]

            glColor3f(d00, d00, d00)
            glVertex2f(x, y)
            glColor3f(d10, d10, d10)
            glVertex2f(x + h, y)
            glColor3f(d11, d11, d11)
            glVertex2f(x + h, y + h)
            glColor3f(d01, d01, d01)
            glVertex2f(x, y + h)
    glEnd()


def get_from_UI(d, u, v):
    global omx, omy
    global dens_prev, u_prev, v_prev

    d[0:size, 0:size] = 0.0

    if not mouse_down[GLUT_LEFT_BUTTON] and not mouse_down[GLUT_RIGHT_BUTTON]:
        return

    i = int((mx / float(win_x)) * N + 1)
    j = int(((win_y - float(my)) / float(win_y)) * float(N) + 1.0)

    if i < 1 or i > N or j < 1 or j > N:
        return

    if mouse_down[GLUT_LEFT_BUTTON]:
        u_prev[i, j] = force * (mx - omx)
        v_prev[i, j] = force * (omy - my)

    if mouse_down[GLUT_RIGHT_BUTTON]:
        d[i, j] = source

    omx = mx
    omy = my


def key_func(key, x, y):
    global dvel

    if key == b'c' or key == b'C':
        clear_data()
    if key == b'v' or key == b'V':
        dvel = not dvel


def mouse_func(button, state, x, y):
    global omx, omy, mx, my, mouse_down

    omx = mx = x
    omy = my = y
    mouse_down[button] = (state == GLUT_DOWN)


def motion_func(x, y):
    global mx, my

    mx = x
    my = y


def reshape_func(width, height):
    global win_x, win_y

    glutReshapeWindow(width, height)
    win_x = width
    win_y = height


def idle_func():
    global dens, dens_prev, u, u_prev, v, v_prev, N, visc, dt, diff
    get_from_UI(dens_prev, u_prev, v_prev)
    vel_step(N, u, v, u_prev, v_prev, visc, dt)
    dens_step(N, dens, dens_prev, u, v, diff, dt)
    glutPostRedisplay()


def display_func():
    pre_display()
    if dvel:
        draw_velocity()
    else:
        draw_density()
    glutSwapBuffers()


def open_glut_window():
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(win_x, win_y)
    glutCreateWindow(b"2D Stable Fluids")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()

    pre_display()

    glutKeyboardFunc(key_func)
    glutMouseFunc(mouse_func)
    glutMotionFunc(motion_func)
    glutReshapeFunc(reshape_func)
    glutIdleFunc(idle_func)
    glutDisplayFunc(display_func)


if __name__ == '__main__':
    glutInit(sys.argv)
    clear_data()
    open_glut_window()
    glutMainLoop()
