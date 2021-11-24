from ctypes import pointer
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import numpy as np

win_x = 400
win_y = 400
g_EnvTemp = 300
step = 0
dt = 0.01
p = []


class Particles:
    def __init__(self, pos, vel, temp, lifetime):
        self.pos = pos
        self.vel = vel
        self.temp = temp
        self.lifetime = lifetime

    def update(self, dt):
        self.vel = 10*(np.array([random.uniform(0.45, 0.55), random.uniform(0.1, 0.6)]) - self.pos)
        self.pos += self.vel * dt
        self.lifetime -= 15*dt
        self.temp -= 5000*(self.temp - g_EnvTemp)*dt

    def draw(self):
        glEnable(GL_POINT_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        if self.temp > g_EnvTemp and self.lifetime > 0:
            glPointSize(self.lifetime)
            glBegin(GL_POINTS)
            glColor4f(1.0, 0.345, 0.101, (self.temp - g_EnvTemp)/(4*g_EnvTemp))
            glVertex2f(self.pos[0], self.pos[1])
            glEnd()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(win_x, win_y)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Fire using Particle System")
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
    global p
    global frame_no
    glClear(GL_COLOR_BUFFER_BIT)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    temp_list = p
    for i in range(len(p)-1, 0, -1):
        p[i].draw() ## Draw particles ##
        if p[i].lifetime <= 0:
            del temp_list[i]
    p = temp_list

    glFlush()  # enforce OpenGL command

    glutSwapBuffers()


def idle():
    global step
    for i in range(len(p)):
        p[i].update(dt) ## Update particle information ##
    step += 1
    glutPostRedisplay()

    for i in range(50):
        pos = np.array([random.uniform(0.4, 0.6), random.uniform(-0.05, 0.05)])
        vel = np.array([random.uniform(0.4, 0.6), 0.5]) - pos
        temp = random.uniform(800, 1000)
        lifetime = random.uniform(5, 20)
        particle = Particles(pos, vel, temp, lifetime)## Create a particle object using the above variables ##
        p.append(particle)


def reshape(width, height):
    global win_x, win_y
    glutReshapeWindow(width, height)
    win_x = width
    win_y = height
    glViewport(0, 0, win_x, win_y)


if __name__ == "__main__":
    main()
