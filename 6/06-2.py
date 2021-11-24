from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import numpy as np

cam_radius = 10.0
cam_pos = [0.0, 2.0, cam_radius]
Lissa_t = 0.0
light_pos = np.array([1.0, 4.0, 0.0])
ambient_light = np.array([0.2, 0.4, 0.4])       # ambient light (k_a * I_a)
k_d = np.array([0.0, 0.6, 0.9])                 # diffuse reflectance
I_q = 5.0                                       # light intensity
g_theta = math.pi/2
g_phi = 0


def draw_axis():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3d(0, 0, 0)
    glVertex3d(1000, 0, 0)        
    glColor3f(0.0, 1.0, 0.0)
    glVertex3d(0, 0, 0)
    glVertex3d(0, 1000, 0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3d(0, 0, 0)
    glVertex3d(0, 0, 1000)        
    glEnd()


def draw_floor():
    glBegin(GL_QUADS)
    glColor4f(0.9, 0.9, 0.9, 1.0)
    glVertex3d(-100, -0.001, 100)
    glVertex3d(100, -0.001, 100)
    glVertex3d(100, -0.001, -100)
    glVertex3d(-100, -0.001, -100)        
    glEnd()

'''
point: a coordinate of a polygon
light: a coordinate of a point light source
xz_plane: y-coordinate of the plane parallel to the xz plane
'''
def calculate_intersection_to_plane(point, light, xz_plane):
    d = point - light
    t = (xz_plane - light[1]) / d[1] if d[1] != 0 else 0
    if t > 0:
        return light + t * d ## calculate intersection point using t and return the coordinate  ##
    else:
        return [math.inf, math.inf, math.inf]

'''
Calculate and draw each shadow on the xz plane created by a point light source for each polygon on a sphere
'''
def draw_sphere_shadow(N, M):
    for j in range(0, N):
        phi = math.pi/2 - j * math.pi / N
        prev_phi = math.pi/2 - (j - 1) * math.pi / N
        for i in range(0, M):
            theta = i * 2 * math.pi / M
            prev_theta = (i - 1) * 2 * math.pi / M
            p00 = np.array([math.sin(theta)*math.sin(phi), math.cos(theta)+2, math.sin(theta)*math.cos(phi)])
            p01 = np.array([math.sin(prev_theta)*math.sin(phi), math.cos(prev_theta)+2, math.sin(prev_theta)*math.cos(phi)])
            p11 = np.array([math.sin(prev_theta)*math.sin(prev_phi), math.cos(prev_theta)+2, math.sin(prev_theta)*math.cos(prev_phi)])
            p10 = np.array([math.sin(theta)*math.sin(prev_phi), math.cos(theta)+2, math.sin(theta)*math.cos(prev_phi)])

            glColor4f(0.1, 0.1, 0.1, 1.0)
            glBegin(GL_QUADS)
            sp00 = calculate_intersection_to_plane(p00, light_pos, 0.0) ## calculate intersection to xz plane using calculate_intersection_to_plane ##
            glVertex3f(sp00[0], sp00[1], sp00[2])
            sp01 = calculate_intersection_to_plane(p01, light_pos, 0.0) ## calculate intersection to xz plane using calculate_intersection_to_plane ##
            glVertex3f(sp01[0], sp01[1], sp01[2])
            sp11 = calculate_intersection_to_plane(p11, light_pos, 0.0) ## calculate intersection to xz plane using calculate_intersection_to_plane ##
            glVertex3f(sp11[0], sp11[1], sp11[2])
            sp10 = calculate_intersection_to_plane(p10, light_pos, 0.0) ## calculate intersection to xz plane using calculate_intersection_to_plane ##
            glVertex3f(sp10[0], sp10[1], sp10[2])
            glEnd()



def calculate_color(point, normal, light, intensity, ambient, diffuse):
    L = light - point
    r = np.linalg.norm(L)
    N = normal/np.linalg.norm(normal) if np.linalg.norm(normal) != 0 else normal
    L = L/r if r != 0 else L

    color = diffuse * intensity * np.dot(L, N)/(r**2) + ambient  if np.dot(L, N) >= 0 else ambient ## Calculate the color based on L, N, r, intensity, diffuse_coefficient and ambient_light. If the surface is hidden surface when looking from light, return only ambient_light ##
#    color = ambient
    return color


def draw_sphere(N, M):
    glColor3f(1.0, 1.0, 1.0)

    for j in range(0, N):
        phi = math.pi/2 - j * math.pi / N
        prev_phi = math.pi/2 - (j - 1)* math.pi / N
        for i in range(0, M):
            theta = i * 2 * math.pi / M
            prev_theta = (i - 1) * 2 * math.pi / M
            p00 = np.array([math.sin(theta)*math.sin(phi), math.cos(theta)+2, math.sin(theta)*math.cos(phi)])
            p01 = np.array([math.sin(prev_theta)*math.sin(phi), math.cos(prev_theta)+2, math.sin(prev_theta)*math.cos(phi)])
            p11 = np.array([math.sin(prev_theta)*math.sin(prev_phi), math.cos(prev_theta)+2, math.sin(prev_theta)*math.cos(prev_phi)])
            p10 = np.array([math.sin(theta)*math.sin(prev_phi), math.cos(theta)+2, math.sin(theta)*math.cos(prev_phi)])

            c00 = calculate_color(p00, p00, light_pos, I_q, ambient_light, k_d)
            c01 = calculate_color(p01, p01, light_pos, I_q, ambient_light, k_d)
            c11 = calculate_color(p11, p11, light_pos, I_q, ambient_light, k_d)
            c10 = calculate_color(p10, p10, light_pos, I_q, ambient_light, k_d)

            glBegin(GL_QUADS)
            glColor3f(c00[0], c00[1], c00[2])
            glVertex3f(p00[0], p00[1], p00[2])

            glColor3f(c01[0], c01[1], c01[2])
            glVertex3f(p01[0], p01[1], p01[2])

            glColor3f(c11[0], c11[1], c11[2])
            glVertex3f(p11[0], p11[1], p11[2])

            glColor3f(c10[0], c10[1], c10[2])
            glVertex3f(p10[0], p10[1], p10[2])


            glEnd()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(400, 400)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"Shadow map")  # show window
    glutDisplayFunc(display)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    glutKeyboardFunc(mykey)          # keyboad callback function
    glutSpecialFunc(mykey)
    init(400, 400)
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
    cam_y = cam_radius * math.cos(g_theta) + 2
    cam_z = cam_radius * math.sin(g_theta) * math.sin(g_phi)
    top = 1.0 if g_theta >= 0.0 else -1.0
    gluLookAt(cam_x, cam_y, cam_z, 0.0, 0.0, 0.0, 0.0, top, 0.0)
    cam_pos = [cam_x, cam_y, cam_z]
#    gluLookAt(0.0, 0.1, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    draw_floor()
    draw_sphere_shadow(50, 50)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    draw_axis()
    draw_sphere(50, 50)    
    glFlush()  # enforce OpenGL command
    glutSwapBuffers()


def idle():
    global Lissa_t, light_pos
    Lissa_t += 0.1
    light_pos = np.array([2*math.sin(3*Lissa_t)+1.0, 4.0, 2*math.sin(4*Lissa_t)])
    glutPostRedisplay()


def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
