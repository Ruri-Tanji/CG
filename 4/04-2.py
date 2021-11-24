from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

win_x = 400
win_y = 400
NX = 128
NY = 128
scalar_field = [[0 for j in range(NY+1)] for i in range(NX+1)]
step = 0
metabo = []
color_map = [[0]*3]*256

class Metaballs:
    def __init__(self, D0, a, init_t):
        self.D0 = D0
        self.a = a
        self.init_t = init_t
        self.x = 0.5*math.cos(init_t)/(1+math.sin(init_t)**2) + 0.5
        self.y = 0.5*math.sin(init_t)*math.cos(init_t)/(1+math.sin(init_t)**2) + 0.5

    def update(self, t):
        self.x = 0.5*math.cos(t+self.init_t)/(1+math.sin(t+self.init_t)**2) + 0.5
        self.y = 0.5*math.sin(t+self.init_t)*math.cos(t+self.init_t)/(1+math.sin(t+self.init_t)**2) + 0.5

'''
calcScalarFieldBy
metaball: list of 2D coordinates at the center of the metaball
r: effective radius
'''
def calcScalarFieldBy(metaball, r):
    global scalar_field

    scalar_field = [[0 for j in range(NY+1)] for i in range(NX+1)]

    for i in range(len(metabo)):
        cx = int(metaball[i].x*NX)
        cy = int(metaball[i].y*NY)
        minx = cx-int(r*NX) if cx-int(r*NX) > 0 else 0
        miny = cy-int(r*NY) if cy-int(r*NY) > 0 else 0
        maxx = cx+int(r*NX) if cx+int(r*NX) < NX else NX
        maxy = cy+int(r*NY) if cy+int(r*NY) < NY else NY
        for ix in range(minx, maxx):
            for iy in range(miny, maxy):
                distance = math.sqrt(((ix - cx)/NX)**2+((iy - cy)/NY)**2)
                if distance <= r:
                    scalar_field[ix][iy] += (metaball[i].D0 * math.exp(-1*metaball[i].a * distance* distance))  ## calculate scalar_field by metaball function ##


def calcColorMap():
    global color_map
    for i in range(256):
        r = 1.0
        g = 0.0
        b = 0.0
        s1 = 119
        s2 = 128
        s3 = 137
        if s3 <= i <= 256:
            r = 0.0
            g = 0.0
            b = 0.5/(256-s3)*(i - s3) + 0.5
        if s2 <= i <= s3:
            r = -1.0/(s3-s2)*(i - s2) + 1.0
            g = -0.5/(s3-s2)*(i - s2) + 0.5
            b = -0.5/(s3-s2)*(i - s2) + 1.0
        if s1 <= i <= s2:
            r = 0.5/(s2-s1)*(i - s1) + 0.5
            g = 0.5/(s2-s1)*(i - s1)
            b = 1.0/(s2-s1)*(i - s1)
        if i <= s1:
            r = -0.5/(s1)*i + 1.0
            g = 0.0
            b = 0.0
        if i == 127:
            r = 0
            g = 0
            b = 0
        color_map[i] = [r, g, b]

'''
draw_2D_ScalarField
sf: scalar field stored in a 2D list.
min: minimum value of scalar field
max: maximum value of scalar field

As shown below, obtain the 255 step values at each vertex of a small square named index__, 
and convert them to RGB values by assigning to a colormap.

index01      index11
      ●------●
      |      |
      |      |
      ●------●
index00      index10
'''
def draw_2D_ScalarField(sf, min, max):
    dx = 1.0/NX
    dy = 1.0/NY
    glBegin(GL_QUADS)
    for i in range(0, NX):
        x = i/NX
        for j in range(0, NY):
            y = j/NY

            index00 = int(255 * (sf[i][j] - min)/(max - min)) if sf[i][j] < max else 255 ## calculate index for color_map based on value of sf[i][j] ##
            glColor3f(color_map[index00][0], color_map[index00][1], color_map[index00][2]) ## specify the color to glColor3f using color_map ##
            glVertex2f(x, y)

            index10 = int(255 * (sf[i+1][j] - min)/(max - min)) if sf[i+1][j] < max else 255
            glColor3f(color_map[index10][0], color_map[index10][1], color_map[index10][2]) ## specify the color to glColor3f using color_map ##
            glVertex2f(x+1, y) ## specify 2D coordinate to glVertex2f ##

            index11 = int(255 * (sf[i+1][j+1] - min)/(max - min)) if sf[i+1][j+1] < max else 255 ## calculate index (index11) for color_map based on value of sf[i+1][j+1] ##
            glColor3f(color_map[index11][0], color_map[index11][1], color_map[index11][2])
            glVertex2f(x+1, y+1) ## specify 2D coordinate to glVertex2f ##

            index01 = int(255 * (sf[i][j+1] - min)/(max - min)) if sf[i][j+1] < max else 255 ## calculate index for color_map based on value of sf[i][j+1] ##
            glColor3f(color_map[index01][0], color_map[index01][1], color_map[index01][2]) ## specify the color to glColor3f using color_map ##
            glVertex2f(x, y+1) ## specify 2D coordinate to glVertex2f ##
    glEnd()

def reshape(width, height):
    global win_x, win_y
    glutReshapeWindow(width, height)
    win_x = width
    win_y = height
    glViewport(0, 0, win_x, win_y)

def idle():
    global step, metabo
    step += 1
    for i in range(len(metabo)):
       metabo[i].update(step/10)
    glutPostRedisplay()

def main():
    global metabo
    # Instantiate the Metaballs class and add to the global list named "metabo"
    m1 = Metaballs(100, 50, 0)
    metabo.append(m1)
    m2 = Metaballs(-100, 50, math.pi)
    metabo.append(m2)
    m3 = Metaballs(100, 50, math.pi/2)
    metabo.append(m3)
    m4 = Metaballs(-100, 50, 3*math.pi/2)
    metabo.append(m4)    

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(win_x, win_y)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"metaball")
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


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Calculate a scalar field from some metaball
    calcScalarFieldBy(metabo, 0.25)

    # Draw a scalar field
    draw_2D_ScalarField(scalar_field, -100, 100)

    glFlush()
    glutSwapBuffers()


if __name__ == "__main__":
    calcColorMap()
    main()
