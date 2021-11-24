from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def drawSquare(x, y, a):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x+a, y)## Use glVertex2f to specify the appropriate coordinates ##
    glVertex2f(x+a, y+a)## Use glVertex2f to specify the appropriate coordinates ##
    glVertex2f(x, y+a)
    glEnd()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Checkerboard")
    glutDisplayFunc(display)
    init()
    glutMainLoop()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    """ gluOrtho2D(left, right, bottom, top) """
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)    # The coordinate system to draw

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    length = 20/400 # Side of a square

    for i in range(0, 20):
        for j in range(0, 20):
            if (i+j)%2==0:## Write the appropriate conditional statement ##
                glColor3f(79/255, 172/255, 135/255)
            else:
                glColor3f(41/255, 37/255, 34/255)
            drawSquare(i*0.05, j*0.05, 0.05)## Call drawSquare function given the correct arguments ##
    glFlush()

if __name__ == "__main__":
    main()
