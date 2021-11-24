from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import math
import os

cam_radius = 5.0
cam_pos = [0.0, 0.0, cam_radius]
im = Image.open(os.path.dirname(__file__)+'dice.png')
g_theta = math.pi/2
g_phi = 0
texID = 0

'''
convert the loaded image (im) to OpenGL texture data
'''
def load_texture():
    w, h = im.size
    rgb_im = im.convert('RGB')
    data = [[[0] * 3 for i in range(h)] for j in range(w)]
    for i in range(w):
        for j in range(h):
            data[h-1-j][i]= rgb_im.getpixel((i,j))## Store the pixel value of rgb_im[][] to data[][] ##


    # Get the texture ID
    tex = glGenTextures(1)
    # Setting to use obtained texture ID
    glBindTexture(GL_TEXTURE_2D, tex)
    # Create texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, data)

    return tex

'''
x, y, z: minimal coordinate of x, y and z in cube respectively
length: length of a cube's edges
'''
def draw_texture_cubic(x, y, z, length):
    # Enabling texture maps
    glEnable(GL_TEXTURE_2D)
    # Set the loaded texture
    glBindTexture(GL_TEXTURE_2D, texID)
    # Specify how to zoom in and out on a texture
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    # look at the origin from z > 0 on z axis
    # 4
    glTexCoord2f(2./3, 1./3)    # Specify the position of the textured image
    glVertex3f(x, y, z)
    glTexCoord2f(1./3, 1./3)    # Specify the position of the textured image
    glVertex3f(x, y, z + length)
    glTexCoord2f(1./3, 2./3)    # Specify the position of the textured image
    glVertex3f(x, y + length, z + length)
    glTexCoord2f(2./3, 2./3)    # Specify the position of the textured image
    glVertex3f(x, y + length, z)

    # 5
    glTexCoord2f(0.0, 1./3)     # Specify the position of the textured image
    glVertex3f(x, y, z)
    glTexCoord2f(1./3, 1./3)    # Specify the position of the textured image
    glVertex3f(x + length, y, z)
    glTexCoord2f(1./3, 2./3)    # Specify the position of the textured image
    glVertex3f(x + length, y + length, z)
    glTexCoord2f(0.0, 2./3)     # Specify the position of the textured image
    glVertex3f(x, y + length, z)    

    # 2
    glTexCoord2f(1./3, 0.0) ## Specify the texture coordinate of the texture using glTexCoord2f ##
    glVertex3f(x + length, y , z + length)## Specify the world coordinate of the quadrangle using glVertex3f and length ##
    glTexCoord2f(2./3, 0.0)     # Specify the position of the textured image
    glVertex3f(x + length, y, z)
    glTexCoord2f(2./3, 1./3)    # Specify the position of the textured image
    glVertex3f(x + length, y + length, z)
    glTexCoord2f(1./3, 1./3)## Specify the texture coordinate of the texture using glTexCoord2f ##
    glVertex3f(x + length, y + length, z + length)


    # 1
    glTexCoord2f(0.0, 0.0)      # Specify the position of the textured image
    glVertex3f(x, y + length, z)
    glTexCoord2f(1./3, 0.0)     # Specify the position of the textured image
    glVertex3f(x, y + length, z + length)
    glTexCoord2f(1./3, 1./3)    # Specify the position of the textured image
    glVertex3f(x + length, y + length, z + length)
    glTexCoord2f(0.0, 1./3)     # Specify the position of the textured image
    glVertex3f(x + length, y + length, z)

    # 3
    glTexCoord2f(2./3, 0.0)     # Specify the position of the textured image
    glVertex3f(x, y, z + length)
    glTexCoord2f(1.0, 0.0)      # Specify the position of the textured image
    glVertex3f(x + length, y, z + length)
    glTexCoord2f(1.0, 1./3)     # Specify the position of the textured image
    glVertex3f(x + length, y + length, z + length)
    glTexCoord2f(2./3, 1./3)    # Specify the position of the textured image
    glVertex3f(x, y + length, z + length)

    # 6
    glTexCoord2f(2./3, 1./3)    # Specify the position of the textured image
    glVertex3f(x, y, z)
    glTexCoord2f(1.0, 1./3)     # Specify the position of the textured image
    glVertex3f(x + length, y, z)
    glTexCoord2f(1.0, 2./3)     # Specify the position of the textured image
    glVertex3f(x + length, y, z + length)
    glTexCoord2f(2./3, 2./3)    # Specify the position of the textured image
    glVertex3f(x, y, z + length)

    
    glEnd()



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


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"Texture mapping")  # show window
    glutDisplayFunc(display)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    glutKeyboardFunc(mykey)          # keyboad callback function
    glutSpecialFunc(mykey)
    init(500, 500)
    glutIdleFunc(idle)
    glutMainLoop()


def init(width, height):
    global texID
    """ initialize """
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST) # enable shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # set perspective
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    texID = load_texture()


def mykey(key, x, y):
    global g_theta, g_phi
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
    r = cam_pos[2]
    cam_x = r*math.sin(g_theta)*math.cos(g_phi)
    cam_y = r*math.cos(g_theta)+cam_pos[1]
    cam_z = r*math.sin(g_theta)*math.sin(g_phi)
    top = 1.0 if g_theta >= 0.0 else -1.0
    gluLookAt(cam_x, cam_y, cam_z, 0.0, cam_pos[1], 0.0, 0.0, top, 0.0)

    draw_axis()
    draw_texture_cubic(0, 0, 0, 1.0)

    glFlush()  # enforce OpenGL command
    glutSwapBuffers()


def idle():
    glutPostRedisplay()


def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)


if __name__ == "__main__":
    main()