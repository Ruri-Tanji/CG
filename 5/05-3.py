from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from PIL import ImageOps
import sys
import math
import numpy as np

cam_radius = 5.0
cam_pos = [0.0, 0.0, cam_radius]
ambient_light = np.array([0.2, 0.2, 0.2])
g_theta = math.pi/3
g_phi = math.pi/2
spotlight = []
sim_time = 0


class Spotlights:
    def __init__(self, pos, color, I0, theta, phi, init_t):
        self.pos = pos          # Position of the spotlight source
        self.init_t = init_t    # Phase
        # Direction of the light source (direction vector from pos)
        self.dir = np.array([math.sin(3*(self.init_t))*math.cos(self.init_t)/2, self.pos[1] - 0.5, math.sin(3*(self.init_t))*math.sin(self.init_t)/2]) - self.pos

        self.color = color
        self.I0 = I0            # Intensity
        self.theta = theta      # Angle for outer-corn range (radian: 0 < theta < pi)
        self.phi = phi          # Angle for inner-corn range (radian: 0 < phi < pi)


    def update(self, t):
        self.dir = np.array([math.sin(3*(t+self.init_t))*math.cos(t+self.init_t)/2, self.pos[1] - 0.5, math.sin(3*(t+self.init_t))*math.sin(t+self.init_t)/2]) - self.pos


    def drawLightDirection(self):
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_LINES)
        glVertex3f(self.pos[0], self.pos[1], self.pos[2])
        glVertex3f(self.dir[0]+self.pos[0], self.dir[1]+self.pos[1], self.dir[2]+self.pos[2])
        glEnd()


    def calcColorFromLight(self, target_pos):
        colored_by_light = np.array([0.0, 0.0, 0.0])
        L2T = target_pos - self.pos                         # Vector from light to target 
        distance = np.linalg.norm(L2T)
        L2T = L2T/distance if distance > 0 else 0           # Normalize L2T
        light_direction = self.dir/np.linalg.norm(self.dir) # Normalize the direction of the light source

        N = np.array([0, 1, 0])
        Lambert = np.dot(N, -L2T)

        if (np.arccos(np.inner(L2T, light_direction)/(np.linalg.norm(L2T)*np.linalg.norm(light_direction)))) <= self.phi/2:## The condition formula that the angle between L2T and light_direction is less than or equal to phi/2 ##
            colored_by_light = Lambert*self.I0*np.array(self.color)/distance**2
            R = 2*N*np.dot(L2T, N)-L2T
            V = R-(2*(N/np.linalg.norm(N)))
            colored_by_light += 1*3*(np.dot(R/np.linalg.norm(R), cam_pos/np.linalg.norm(cam_pos))**10)
            
        if ((np.arccos(np.inner(L2T, light_direction)/(np.linalg.norm(L2T)*np.linalg.norm(light_direction)))) <= self.theta/2) and (np.arccos(np.inner(L2T, light_direction)/(np.linalg.norm(L2T)*np.linalg.norm(light_direction)))) >= self.phi/2:## The condition formula that the angle between L2T and light_direction is less than or equal to theta/2 and more than phi/2 ##
            decay = (np.dot(L2T, light_direction) - np.cos(self.theta/2))/(np.cos(self.phi/2) - np.cos(self.theta/2))
            colored_by_light =  Lambert*decay*self.I0*np.array(self.color)/distance**2
        return colored_by_light


'''

drawFloor
draw the plane -2 <= x <= 2, y = -1, -2 <= z <= 2.
N, M: Number of divisions along x-axis or z-axis
The number of small square is N*M.

p01      p11
  ●------●
  |      |
  |      |
  ●------●
p00      p10
'''
def drawFloor(N, M):
    dx = 4 / N
    dz = 4 / M
    for j in range(0, N):
        for i in range(0, M):
            p00 = np.array([-2.0+dx*j,     -1.0, -2.0+dz*i])
            p10 = np.array([-2.0+dx*(j+1), -1.0, -2.0+dz*i])
            p11 = np.array([-2.0+dx*(j+1), -1.0, -2.0+dz*(i+1)])
            p01 = np.array([-2.0+dx*j,     -1.0, -2.0+dz*(i+1)])

            c00 = c10 = c11 = c01 = np.array(ambient_light)

            for k in range(len(spotlight)):
                c00 += spotlight[k].calcColorFromLight(p00) ## Call the function in Spotlights class to calculate the color c00 at p00. ##
                c10 += spotlight[k].calcColorFromLight(p10) ## Call the function in Spotlights class to calculate the color c10 at p10. ##
                c11 += spotlight[k].calcColorFromLight(p11) ## Call the function in Spotlights class to calculate the color c11 at p11. ##
                c01 += spotlight[k].calcColorFromLight(p01) ## Call the function in Spotlights class to calculate the color c01 at p01. ##

            glBegin(GL_QUADS)
            glColor3f(c00[0], c00[1], c00[2])
            glVertex3f(p00[0], p00[1], p00[2])

            glColor3f(c10[0], c10[1], c10[2])
            glVertex3f(p10[0], p10[1], p10[2])

            glColor3f(c11[0], c11[1], c11[2])
            glVertex3f(p11[0], p11[1], p11[2])

            glColor3f(c01[0], c01[1], c01[2])
            glVertex3f(p01[0], p01[1], p01[2])
            glEnd()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(400, 400)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"Spotlight")  # show window
    glutDisplayFunc(display)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    glutKeyboardFunc(mykey)          # keyboad callback function
    glutSpecialFunc(mykey)
    init(400, 400)

    global spotlight
    light_pos = np.array([0.0, 2.0, 0.0]) #点光源
    color1 = [1.0, 0.0, 0.0]
    sl1 = Spotlights(light_pos, color1, 5.0, math.pi/4, math.pi/15, 0)
    spotlight.append(sl1)
    color2 = [0.0, 1.0, 0.0]
    sl2 = Spotlights(light_pos, color2, 5.0, math.pi/4, math.pi/15, 2*math.pi/3)
    spotlight.append(sl2)
    color3 = [0.0, 0.0, 1.0]
    sl3 = Spotlights(light_pos, color3, 5.0, math.pi/4, math.pi/15, 4*math.pi/3)
    spotlight.append(sl3)
    glutIdleFunc(idle)
    glutMainLoop()


def init(width, height):
    """ initialize """
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST) # enable shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # set perspective
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)


def mykey(key, x, y):
    global g_theta, g_phi, draw_line_flag
    if key == GLUT_KEY_RIGHT:
        g_phi -= 0.1
    if key == GLUT_KEY_LEFT:
        g_phi += 0.1    
    if key == GLUT_KEY_UP:
        g_theta -= 0.1
        if g_theta < -math.pi:
            g_theta = math.pi
    if key == GLUT_KEY_DOWN:
        g_theta += 0.1
        if g_theta > math.pi:
            g_theta = -math.pi


def display():
    """ display """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
   # set camera
    global cam_pos
    cam_x = cam_radius * math.sin(g_theta) * math.cos(g_phi)
    cam_y = cam_radius * math.cos(g_theta)
    cam_z = cam_radius * math.sin(g_theta) * math.sin(g_phi)
    top = 1.0 if g_theta >= 0.0 else -1.0
    gluLookAt(cam_x, cam_y, cam_z, 0.0, 0.0, 0.0, 0.0, top, 0.0)
    cam_pos = [cam_x, cam_y, cam_z]
    for i in range(len(spotlight)):
        spotlight[i].drawLightDirection()

#    drawFloor(150, 150)
    drawFloor(20, 20)      # for debug

    glFlush()  # enforce OpenGL command
    glutSwapBuffers()


def idle():
    global sim_time
    sim_time += 0.01
    for i in range(len(spotlight)):
        spotlight[i].update(sim_time)
    glutPostRedisplay()


def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
