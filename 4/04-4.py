from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import os
import numpy as np
import time


T=0
cam_pos = [0.0, 0.1, 0.4]
theta = math.pi/2
phi = math.pi/4
vertices = []
uvs = []
normals = []
vertexColors = []
faceVertIDs = []
uvIDs = []
normalIDs = []
draw_line_flag = False


def key_func(n):
    return n[0]

def calcColorMap(x):
    leng=abs(x_max-x_min)
    x=abs(x-x_min)/leng+T
    if x>1:
        x=x%1
    r = 1.0
    g = 0.0
    b = 0.0
    if x <= 1:
        r = 1.0
        g = 0.0
        b = 1.0 - (x - 5.0/6.0)*6.0
    if x <= 5.0/6.0:
        r = 6.0*(x - 4.0/6.0)
        g = 0.0
        b = 1.0
    if x <= 4.0/6.0:
        r = 0.0
        g = 1.0 - (x - 3.0/6.0)*6.0
        b = 1.0
    if x <= 3.0/6.0:
        r = 0.0
        g = 1.0
        b = 6.0*(x - 2.0/6.0)
    if x <= 2.0/6.0:
        r = 1.0 - (x - 1.0/6.0)*6.0
        g = 1.0
        b = 0.0
    if x <= 1.0/6.0:
        r = 1.0
        g = 6.0*x
        b = 0.0

    return glColor3f(r,g,b)


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


def loadOBJ(fliePath):
    numVertices = 0
    numUVs = 0
    numNormals = 0
    numFaces = 0
    global vertices
    global uvs
    global normals
    global vertexColors
    global faceVertIDs
    global uvIDs
    global normalIDs
    global min_x
    global max_x

    for line in open(fliePath, "r"):
        vals = line.split()
        if len(vals) == 0:
            continue
        if vals[0] == "v":
            v = list(map(float,vals[1:4]))
            vertices.append(v)
            numVertices += 1
            if len(vals) == 7:
                vc = list(map(float,vals[4:7]))
                vertexColors.append(vc)
        if vals[0] == "vt":
            vt = list(map(float,vals[1:3]))
            uvs.append(vt)
            numUVs += 1
        if vals[0] == "vn":
            vn = list(map(float,vals[1:4]))
            normals.append(vn)
            numNormals += 1
        if vals[0] == "f":
            fvID = []
            uvID = []
            nvID = []
            for f in vals[1:]:
                w = f.split("/")
                if numVertices > 0:
                    w[0] = int(w[0])
                    fvID.append(abs(w[0])-1)
                if numUVs > 0:
                    uvID.append(int(w[1])-1)
                if numNormals > 0:
                    nvID.append(int(w[2])-1)
            faceVertIDs.append(fvID)
            uvIDs.append(uvID)
            normalIDs.append(nvID)
            numFaces += 1
    min_x=min(faceVertIDs, key=key_func)
    max_x=max(faceVertIDs, key=key_func)
    print("#Vertices: ", numVertices)
    print("#UVs: ", numUVs)
    print("#Normals: ", numNormals)
    print("#Faces: ", numFaces)
    print (min_x[0])
    print (max_x[0])
    


def length():
    global x_max
    global x_min
    x_max=vertices[faceVertIDs[0][0]][0]
    x_min=vertices[faceVertIDs[0][0]][0]
    for j in range(0, len(faceVertIDs)):
        for i in range(0, 3):
            if x_max <= vertices[faceVertIDs[j][i]][0]:
                x_max = vertices[faceVertIDs[j][i]][0]
                if x_min >= vertices[faceVertIDs[j][i]][0]:
                    x_min = vertices[faceVertIDs[j][i]][0]
            else:
                if x_min >= vertices[faceVertIDs[j][i]][0]:
                    x_min = vertices[faceVertIDs[j][i]][0]

    

def draw_polygon():
      
    glBegin(GL_TRIANGLES)
    for j in range(0, len(faceVertIDs)):
        for i in range(0, 3):
            calcColorMap(vertices[faceVertIDs[j][i]][0])
            glVertex3f(vertices[faceVertIDs[j][i]][0], vertices[faceVertIDs[j][i]][1], vertices[faceVertIDs[j][i]][2])
    glEnd()

    if draw_line_flag == True:
        glColor3f(1.0, 0.65, 0.0)
        for j in range(0, len(faceVertIDs)):
            glBegin(GL_LINE_STRIP) 
            for i in range(0, 3):
                glVertex3f(vertices[faceVertIDs[j][i]][0], vertices[faceVertIDs[j][i]][1], vertices[faceVertIDs[j][i]][2])
            glEnd()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)     # window size
    glutInitWindowPosition(100, 100) # window position
    glutCreateWindow(b"OBJ loader")  # show window
    glutDisplayFunc(display)         # draw callback function
    glutReshapeFunc(reshape)         # resize callback function
    glutKeyboardFunc(mykey)          # keyboad callback function
    glutSpecialFunc(mykey)
    init(500, 500)
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
    loadOBJ(os.path.dirname(os.path.abspath(__file__))+"/obj/bunny.obj")


def mykey(key, x, y):
    global theta, phi, draw_line_flag
    if key == GLUT_KEY_RIGHT:
        phi -= 0.1
    if key == GLUT_KEY_LEFT:
        phi += 0.1    
    if key == GLUT_KEY_UP:
        theta -= 0.1
        if theta < -math.pi:
            theta = math.pi
    if key == GLUT_KEY_DOWN:
        theta += 0.1
        if theta > math.pi:
            theta = -math.pi
    if key == b'l':
        draw_line_flag = not draw_line_flag

def display():
    """ display """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    length()
    # set camera
    r = cam_pos[2]
    cam_x = r*math.sin(theta)*math.cos(phi)
    cam_y = r*math.cos(theta)+cam_pos[1]
    cam_z = r*math.sin(theta)*math.sin(phi)
    top = 1.0 if theta >= 0.0 else -1.0
    gluLookAt(cam_x, cam_y, cam_z, 0.0, cam_pos[1], 0.0, 0.0, top, 0.0)

    draw_axis()

    # draw polygons of object
    draw_polygon()

    glFlush()  # enforce OpenGL command
    glutSwapBuffers()

def idle():
    global T
    time.sleep(0.1)
    T +=0.1
    glutPostRedisplay()
    glutIdleFunc(idle)


def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
