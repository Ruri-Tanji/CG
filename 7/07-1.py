from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import numpy as np
import math
import sys

win_x = 400
win_y = 400
step = 0
dt = 0.02
bird = []
bird_num = 15
R = 0.4
max_theta = 5*math.pi/6
min_theta = -5*math.pi/6


class Birds:
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel

    def update(self, index, dt):
        vl = create_visible_list(index)
        self.vel += 0.01*cohesion_rule(index, vl) + 0.09*alignment_rule(index, vl) + 0.9*separation_rule(index, vl)
        self.vel = 0.1 * self.vel / np.linalg.norm(self.vel) if np.linalg.norm(self.vel) != 0 else self.vel
        self.x += self.vel[0] * dt
        self.y += self.vel[1] * dt
        if self.x < 0.0:
            self.x += 1.0
        if self.y < 0.0:
            self.y += 1.0
        if self.x > 1.0:
            self.x -= 1.0
        if self.y > 1.0:
            self.y -= 1.0

    def draw(self, timestep):
        glColor3f(0.72, 0.82, 0.0)
        draw_elipse(self.x, self.y, 0.03, 0.01, math.atan2(self.vel[1], self.vel[0]))
        draw_wings(self.x, self.y, math.atan2(self.vel[1], self.vel[0]), timestep)


def draw_elipse(x, y, a, b, angle):
    glBegin(GL_POLYGON)
    dtheta = 0
    while dtheta < 2*math.pi:
        dx = a*math.cos(dtheta)
        dy = b*math.sin(dtheta)

        px = dx * math.cos(angle) - dy * math.sin(angle) + x
        py = dx * math.sin(angle) + dy * math.cos(angle) + y

        glVertex2f(px, py)

        dtheta += math.pi/30
    glEnd()


def draw_wings(x, y, angle, step):
    wing = [[0.01, 0.0], [0.01, 0.02], [-0.03, 0.03], [0., 0.01], [0., -0.01], [-0.03, -0.03], [0.01, -0.02]]
    tail = [[-0.02, 0.0], [-0.035, 0.015], [-0.035, -0.015]]
    beak = [[0.033, 0.0], [0.03, 0.002], [0.03, -0.002]]

    if step % 250 < 125:
        wing = [[0.01, 0.0], [0.01, 0.03], [-0.005, 0.015], [-0.005, -0.015], [0.01, -0.03]]
    glBegin(GL_TRIANGLE_FAN)
    for i in range(len(wing)):
        px = wing[i][0] * math.cos(angle) - wing[i][1] * math.sin(angle) + x
        py = wing[i][0] * math.sin(angle) + wing[i][1] * math.cos(angle) + y
        glVertex2f(px, py)
    glEnd()
    glBegin(GL_TRIANGLES)
    for i in range(len(tail)):
        px = tail[i][0] * math.cos(angle) - tail[i][1] * math.sin(angle) + x
        py = tail[i][0] * math.sin(angle) + tail[i][1] * math.cos(angle) + y
        glVertex2f(px, py)
    for i in range(len(beak)):
        px = beak[i][0] * math.cos(angle) - beak[i][1] * math.sin(angle) + x
        py = beak[i][0] * math.sin(angle) + beak[i][1] * math.cos(angle) + y
        glVertex2f(px, py)
    glEnd()

def judge_visible(main_index, target_index, radius, max_angle, min_angle):
    tx = bird[target_index].x - bird[main_index].x
    ty = bird[target_index].y - bird[main_index].y
    main_angle = math.atan2(bird[main_index].y, bird[main_index].x)
    target_angle = math.atan2(bird[target_index].y, bird[target_index].x)
    return True if (tx**2+ty**2)**0.5 <= R and min_angle <= target_angle - main_angle <= max_angle else False


def create_visible_list(bird_index):
    visible_list = []
    for i in range(len(bird)):
        if i != bird_index:
            if judge_visible(bird_index, i, R, max_theta, min_theta):
                visible_list.append(i)
    return visible_list

def cohesion_rule(bird_index, visible_list):
    average_pos = np.zeros(2)
    for i in range(len(visible_list)):
        average_pos[0] += bird[visible_list[i]].x
        average_pos[1] += bird[visible_list[i]].y
    average_pos /= len(visible_list) if len(visible_list) != 0 else 1
    vec_cohesion = (average_pos-np.array([bird[bird_index].x, bird[bird_index].y])) / np.linalg.norm(average_pos-np.array([bird[bird_index].x, bird[bird_index].y])) if np.linalg.norm(average_pos-np.array([bird[bird_index].x, bird[bird_index].y])) != 0 else average_pos-np.array([bird[bird_index].x, bird[bird_index].y])## calculate vec_cohesion ##
    #print(np.array([bird[bird_index].x, bird[bird_index].y]))
    return vec_cohesion


def alignment_rule(bird_index, visible_list):
    average_vel = np.zeros(2)
    for i in range(len(visible_list)):
        average_vel += bird[visible_list[i]].vel
    average_vel /= len(visible_list) if len(visible_list) != 0 else 1
    vec_alignment = (average_vel) / np.linalg.norm(average_vel) if np.linalg.norm(average_vel)  != 0 else average_vel  ## calculate vec_alignment ##
    #print(bird[bird_index].vel)
    return vec_alignment 

def separation_rule(bird_index, visible_list):
    sum_vel = np.zeros(2)
    main_x = bird[bird_index].x
    main_y = bird[bird_index].y
    for i in range(len(visible_list)):
        distance = ((bird[visible_list[i]].x - main_x)**2 + (bird[visible_list[i]].y - main_y)**2)**0.5
        if distance < R*0.2:
            sum_vel +=  np.array([(main_x - bird[visible_list[i]].x), (main_y - bird[visible_list[i]].y)]) / distance**2  ## add a separation vector to sum_vel that is inversely proportional to the square of the distance ##
    sum_vel /= len(sum_vel) if len(sum_vel) != 0 else 1
    vec_separation = sum_vel / np.linalg.norm(sum_vel) if np.linalg.norm(sum_vel) != 0 else sum_vel ## let vec_separation be the vector by normalizing sum_vel ##
    #print(vec_separation)
    return vec_separation

def reshape(width, height):
    global win_x, win_y
    glutReshapeWindow(width, height)
    win_x = width
    win_y = height
    glViewport(0, 0, win_x, win_y)


def idle():
    global step
    step += 1
    for i in range(bird_num):
        bird[i].update(i, dt)
    glutPostRedisplay()


def main():
    global bird
    # instantiate & add the object to list (bird)
    for i in range(bird_num):
        b = Birds(random.random(), random.random(), np.array([random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)]))
        bird.append(b)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
    glutInitWindowSize(win_x, win_y)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Boids algorithm")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    init()
    glutIdleFunc(idle)
    glutMainLoop()


def init():
    glViewport(0, 0, win_x, win_y)
    glClearColor(0.67, 0.91, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    """ gluOrtho2D(left, right, bottom, top) """
    gluOrtho2D(0.0, 1.0, 0.0, 1.0)    # The coordinate system to draw


def display():
    global frame_no
    glClear(GL_COLOR_BUFFER_BIT)
    for i in range(bird_num):
        bird[i].draw(step)
    glFlush()
    glutSwapBuffers()


if __name__ == "__main__":
    main()
