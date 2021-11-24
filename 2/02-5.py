from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

mercury_angle = 0.0
venus_angle = 0.0
earth_angle = 0.0
moon_angle = 0.0
mars_angle = 0.0

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"3D")      # show window
    init(300,300)
    glutDisplayFunc(display)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    glutIdleFunc(idle)
    glutMainLoop()

def init(width, height):
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

def display():
    """ display """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    # 太陽
    glColor3f(1.0, 0.0, 0.0)
    glutSolidSphere(0.3, 20, 20)

    # 水星
    glPushMatrix()
    glColor3f(0.6, 0.6, 0.6)
    glRotatef(mercury_angle, 0.0, 1.0, 0.0)
    glTranslatef(0.5, 0.0, 0.0)
    glutSolidSphere(0.15, 20, 20)
    glPopMatrix()
    
    # 金星
    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)
    glRotatef(venus_angle, 0.0, 1.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glutSolidSphere(0.15, 20, 20)
    glPopMatrix()

    # 火星
    glPushMatrix()
    glColor3f(0.8, 0.6, 0.4)
    glRotatef(mars_angle, 0.0, 1.0, 0.0)
    glTranslatef(2.4, 0.0, 0.0)
    glutSolidSphere(0.15, 20, 20)
    glPopMatrix()

    # 地球
    glRotatef(earth_angle, 0.0, 1.0, 0.0)
    glTranslatef(1.7, 0.0, 0.0)
    glColor3f(0.4, 0.4, 0.8)
    glutSolidSphere(0.2, 20, 20)
    
    # 月
    glColor3f(1.0, 1.0, 0.6)
    glRotatef(moon_angle, 0.0, 1.0, 0.0)
    glTranslatef(0.4, 0.0, 0.0)
    glutSolidSphere(0.1, 20, 20)
    
    glutSwapBuffers()
    
    glFlush()  # enforce OpenGL command

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def idle():
    global mercury_angle, venus_angle, earth_angle, moon_angle, mars_angle
    mercury_angle += 0.114
    venus_angle += 0.044
    earth_angle += 0.027
    moon_angle += 0.370
    mars_angle += 0.015
    glutPostRedisplay()

if __name__ == "__main__":
    main()
