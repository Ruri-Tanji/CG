from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math
import os

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

class PlyModel(object):
    def __init__(self):
        self.vertices = [] # [(x,y,z)]
        self.faces = [] # [(xi,yi,zi)]
        self.nvertex = None
        self.nface = None
        self.maxx = -1e10
        self.maxy = -1e10
        self.maxz = -1e10
    def load(self, filepath):
        global cam_x,cam_y,cam_z
        f = open(filepath, "rb")
        # read header
        while True:
            lst = f.readline().split()
            if lst[0] == "end_header":
                break
            if lst[0] == "element":
                if lst[1] == "vertex":
                    self.nvertex = int(lst[2])
                if lst[1] == "face":
                    self.nface = int(lst[2])
        # read vertex
        for i in xrange(self.nvertex):
            v = map(float, f.readline().split()[:3])
            self.maxx = max(self.maxx, v[0])
            self.maxy = max(self.maxy, v[1])
            self.maxz = max(self.maxz, v[2])
            self.vertices.append(v)
        # read face
        for i in xrange(self.nface):
            x = map(int, f.readline().split()[1:])
            self.faces.append(x)
        f.close()
    def draw(self):
        # 面法線を設定して描画する
        glBegin(GL_TRIANGLES)
        for index in self.faces:
            p1,p2,p3 = map(lambda i: self.vertices[i], index)
            u = map(lambda x,y: x-y, p2, p1)
            v = map(lambda x,y: x-y, p3, p1)
            cross = ( # 法線の計算
                u[1]*v[2] - u[2]*v[1],
                u[2]*v[0] - u[0]*v[2],
                u[0]*v[1] - u[1]*v[0],
                )
            # 正規化
            norm = sum(map(lambda x:x*x, cross))**.5
            cross = map(lambda x:x/norm, cross)
            glNormal3fv(cross)
            glVertex3fv(p1)
            glVertex3fv(p2)
            glVertex3fv(p3)
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

    for line in open(fliePath, "r"):
        vals = line.split()
        if len(vals) == 0:
            continue
        if vals[0] == "v":
            v =  list(map(float,vals[1:4])) ## convert string to float and change type to list ##
            vertices.append(v)
            numVertices += 1
            if len(vals) == 7:
                vc = list(map(float,vals[4:7])) ## convert string to float and change type to list ##
                vertexColors.append(vc)
        if vals[0] == "vt":
            vt = list(map(float,vals[1:3])) ## convert string to float and change type to list ##
            uvs.append(vt)
            numUVs += 1
        if vals[0] == "vn":
            vn = list(map(float,vals[1:4])) ## convert string to float and change type to list ##
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
    print("#Vertices: ", numVertices)
    print("#UVs: ", numUVs)
    print("#Normals: ", numNormals)
    print("#Faces: ", numFaces)


def draw_polygon():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_TRIANGLES)
    for j in range(0, len(faceVertIDs)):
        for i in range(0, 3):
            glVertex3f(vertices[faceVertIDs[j][i]][0], vertices[faceVertIDs[j][i]][1], vertices[faceVertIDs[j][i]][2])
    glEnd()

    if draw_line_flag == True:
        glColor3f(1.0, 0.65, 0.0)
        for j in range(0, len(faceVertIDs)):
            glBegin(GL_LINE_STRIP) ## glBegin(____________) ##
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
    global displist,cx,cy,cz
    glClearColor(1,1,1,1)
    glEnable(GL_DEPTH_TEST) # enable shading

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [200,300,105,0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [.1,.1,.1,1])
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # set perspective
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
    loadOBJ(os.path.dirname(os.path.abspath(__file__))+"/obj/bunny.obj")

    ply = PlyModel()
    ply.load(sys.argv[1])
    displist = glGenLists(1)
    glNewList(displist, GL_COMPILE)
    ply.draw()
    glEndList()


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
    glutPostRedisplay()

def reshape(width, height):
    """callback function resize window"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)

if __name__ == "__main__":
    main()
