import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtCore, QtGui, QtOpenGL, QtWidgets
import cube3solver as cubes


class GLDemo(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.running = 0
        self.speed = 6
        self.xsize = 400
        self.ysize = 400
        self.view_x = 0
        self.view_y = 0
        self.view_z = 0
        self.currentmove = [0, 0, 0, 0, 0, 0]
        self.currentrotation = 0
        self.currentangle = 0
        self.cube3 = cubes.Cube3()
        self.cube3_dup = cubes.Cube3()
        self.movement_list = []
        self.backward_list = []
        self.block_pos = [
            [-1, 1, 1],
            [0, 1, 1],
            [1, 1, 1],
            [-1, 0, 1],
            [0, 0, 1],
            [1, 0, 1],
            [-1, -1, 1],
            [0, -1, 1],
            [1, -1, 1],

            [-1, 1, 0],
            [0, 1, 0],
            [1, 1, 0],
            [-1, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
            [-1, -1, 0],
            [0, -1, 0],
            [1, -1, 0],

            [-1, 1, -1],
            [0, 1, -1],
            [1, 1, -1],
            [-1, 0, -1],
            [0, 0, -1],
            [1, 0, -1],
            [-1, -1, -1],
            [0, -1, -1],
            [1, -1, -1]
        ]

        self.rotate_ack = [
            [0, 1, 1, 0, 0, 1],
            [0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0],

            [0, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [1, 0, 0, 0, 1, 0],

            [0, 1, 0, 1, 0, 1],
            [0, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 0],
            [0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0],
        ]

        self.block_color = [
            [[3, 0, 0], [4, 0, 2], [5, 0, 0]],
            [[3, 0, 0], [4, 0, 1], [5, 0, 1]],
            [[2, 0, 2], [4, 0, 0], [5, 0, 2]],
            [[3, 0, 1], [4, 0, 2], [5, 1, 0]],
            [[3, 0, 0], [4, 0, 2], [5, 1, 1]],
            [[2, 0, 1], [4, 0, 2], [5, 1, 2]],
            [[3, 0, 2], [1, 0, 0], [5, 2, 0]],
            [[3, 0, 0], [1, 0, 1], [5, 2, 1]],
            [[2, 0, 0], [1, 0, 2], [5, 2, 2]],

            [[3, 1, 0], [4, 1, 2], [5, 0, 0]],
            [[3, 1, 0], [4, 1, 1], [5, 0, 1]],
            [[2, 1, 2], [4, 1, 0], [5, 0, 2]],
            [[3, 1, 1], [4, 1, 2], [5, 1, 0]],
            [[3, 1, 0], [4, 1, 2], [5, 1, 1]],
            [[2, 1, 1], [4, 1, 2], [5, 1, 2]],
            [[3, 1, 2], [1, 1, 0], [5, 2, 0]],
            [[3, 1, 0], [1, 1, 1], [5, 2, 1]],
            [[2, 1, 0], [1, 1, 2], [5, 2, 2]],

            [[3, 2, 0], [4, 2, 2], [0, 0, 0]],
            [[3, 2, 0], [4, 2, 1], [0, 0, 1]],
            [[2, 2, 2], [4, 2, 0], [0, 0, 2]],
            [[3, 2, 1], [4, 2, 2], [0, 1, 0]],
            [[3, 2, 0], [4, 2, 2], [0, 1, 1]],
            [[2, 2, 1], [4, 2, 2], [0, 1, 2]],
            [[3, 2, 2], [1, 2, 0], [0, 2, 0]],
            [[3, 2, 0], [1, 2, 1], [0, 2, 1]],
            [[2, 2, 0], [1, 2, 2], [0, 2, 2]],
        ]

        self.color_scheme = [
            [255, 255, 255],
            [239, 62, 52],
            [0, 173, 81],
            [57, 183, 234],
            [254, 135, 7],
            [244, 245, 1]
        ]

        self.single_step = 1
        self.backwards = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.animation)
        self.timer.start(1)

    def initializeGL(self):
        glClearColor(1, 1, 1, 1)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)

    def mySolidCube(self, size):
        size /= 2
        glBegin(GL_POLYGON)
        glVertex3f(size, -size, -size)
        glVertex3f(size,  size, -size)
        glVertex3f(-size,  size, -size)
        glVertex3f(-size, -size, -size)
        glEnd()

        glBegin(GL_POLYGON)
        glVertex3f(size, -size, size)
        glVertex3f(size,  size, size)
        glVertex3f(-size,  size, size)
        glVertex3f(-size, -size, size)
        glEnd()

        glBegin(GL_POLYGON)
        glVertex3f(size, -size, -size)
        glVertex3f(size,  size, -size)
        glVertex3f(size,  size,  size)
        glVertex3f(size, -size,  size)
        glEnd()

        glBegin(GL_POLYGON)
        glVertex3f(-size, -size,  size)
        glVertex3f(-size,  size,  size)
        glVertex3f(-size,  size, -size)
        glVertex3f(-size, -size, -size)
        glEnd()

        glBegin(GL_POLYGON)
        glVertex3f(size,  size,  size)
        glVertex3f(size,  size, -size)
        glVertex3f(-size,  size, -size)
        glVertex3f(-size,  size,  size)
        glEnd()

        glBegin(GL_POLYGON)
        glVertex3f(size, -size, -size)
        glVertex3f(size, -size,  size)
        glVertex3f(-size, -size,  size)
        glVertex3f(-size, -size, -size)
        glEnd()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)

        for block in range(27):
            glPushMatrix()
            glLoadIdentity()
            gluPerspective(90, 1, 0.01, 100)
            gluLookAt(1, -1, 1, 0, 0, 0, 0, 1, 1)
            glRotate(self.view_x, 1, 0, 0)
            glRotate(self.view_y, 0, 1, 0)
            glRotate(self.view_z, 0, 0, 1)
            axis_x = self.currentmove[0]*self.rotate_ack[block][0] + \
                self.currentmove[1]*self.rotate_ack[block][1]
            axis_y = self.currentmove[4]*self.rotate_ack[block][4] + \
                self.currentmove[5]*self.rotate_ack[block][5]
            axis_z = self.currentmove[2]*self.rotate_ack[block][2] + \
                self.currentmove[3] * \
                self.rotate_ack[block][3]+self.currentrotation
            glRotate(self.currentangle*(axis_x+axis_y+axis_z),
                     abs(axis_x), abs(axis_y), abs(axis_z))
            glTranslate(0.3*self.block_pos[block][0], 0.3 *
                        self.block_pos[block][1], 0.3*self.block_pos[block][2])
            glColor3f(0, 0, 0)
            self.mySolidCube(0.28)
            glTranslate(0.02*self.block_pos[block][0], 0, 0)
            glColor3ubv(self.color_scheme[self.cube3.cube[self.block_color[block][0][0]]
                                          [self.block_color[block][0][1]][self.block_color[block][0][2]]])
            self.mySolidCube(0.26)
            glTranslate(-0.02*self.block_pos[block]
                        [0], 0.02*self.block_pos[block][1], 0)
            glColor3ubv(self.color_scheme[self.cube3.cube[self.block_color[block][1][0]]
                                          [self.block_color[block][1][1]][self.block_color[block][1][2]]])
            self.mySolidCube(0.26)
            glTranslate(
                0, -0.02*self.block_pos[block][1], 0.02*self.block_pos[block][2])
            glColor3ubv(self.color_scheme[self.cube3.cube[self.block_color[block][2][0]]
                                          [self.block_color[block][2][1]][self.block_color[block][2][2]]])
            self.mySolidCube(0.26)
            glPopMatrix()

        glFlush()

    def resizeGL(self, width, height):
        if height == 0:
            height = 1
        if width == 0:
            width = 1
        if width == height:
            glViewport(0, 0, width, height)
        elif width > height:
            glViewport(round((width-height)/2), 0, height, height)
        else:
            glViewport(0, round((height-width)/2), width, width)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

    def button_scramble(self):
        self.speed = 9
        if(self.running == 1):
            return
        self.running = 1
        self.movement_list = self.cube3_dup.scramble().split()
        print(self.movement_list)
        self.backward_list = []
        self.running = 0

    def button_cfop(self):
        self.speed = 6
        if(self.running == 1):
            return
        self.running = 1
        
        self.movement_list = []
        self.cube3_dup.input_raw(self.cube3.cube)
        algs = self.cube3_dup.full_cfop()
        for i in algs:
            self.movement_list += i.split()
        print(self.movement_list)
        self.backward_list = []
        self.running = 0

    # add
    def button_valid(self):
        self.speed = 3
        if(self.running == 1):
            return
        self.running = 1
        self.cube3_dup.input_raw(self.cube3.cube)
        now_cube = self.cube3_dup
        step_algorithm = []
        self.movement_list = []
        if now_cube.cross_done() == False:
            print("First Mission: Cross!")
            algs = now_cube.cfop_cross()
            print(algs)
            step_algorithm.append(algs)
        elif now_cube.f2l_done() == False:
            print("Second Mission: F2L(First Two Layers)!")
            algs = now_cube.cfop_f2l()
            print(algs)
            step_algorithm.append(algs)
        elif now_cube.oll_done() == False:
            print("Third Mission: OLL(Orientation Of Last Layer))!")
            algs = now_cube.cfop_oll()
            print(algs)
            step_algorithm.append(algs)
        elif now_cube.cfop_done() == False:
            print("Forth Mission: PLL(Permutation of Last Layer)!")
            algs = now_cube.cfop_pll()
            print(algs)
            step_algorithm.append(algs)
        else:
            print("The cube has been solved!")

        for i in step_algorithm:
            self.movement_list += i.split()
        if(len(self.movement_list)!=0):
            print(str(len(self.movement_list)) + " steps remaining to accomplish this mission.")
        self.backward_list = []
        self.running = 0


    def upButton(self):
        self.view_x -= 10

    def leftButton(self):
        self.view_y += 10

    def downButton(self):
        self.view_x += 10

    def rightButton(self):
        self.view_y -= 10

    def getmove(self, back):
        move = ''

        if back == 0:
            if len(self.movement_list) != 0:
                move = self.movement_list[0]
        else:
            if len(self.backward_list) != 0:
                move = self.backward_list[-1]

        if move == 'R':
            self.currentmove = [-1, 0, 0, 0, 0, 0]
        if move == 'R_':
            self.currentmove = [1, 0, 0, 0, 0, 0]
        if move == 'L':
            self.currentmove = [0, 1, 0, 0, 0, 0]
        if move == 'L_':
            self.currentmove = [0, -1, 0, 0, 0, 0]
        if move == 'U':
            self.currentmove = [0, 0, -1, 0, 0, 0]
        if move == 'U_':
            self.currentmove = [0, 0, 1, 0, 0, 0]
        if move == 'D':
            self.currentmove = [0, 0, 0, 1, 0, 0]
        if move == 'D_':
            self.currentmove = [0, 0, 0, -1, 0, 0]
        if move == 'F':
            self.currentmove = [0, 0, 0, 0, 1, 0]
        if move == 'F_':
            self.currentmove = [0, 0, 0, 0, -1, 0]
        if move == 'B':
            self.currentmove = [0, 0, 0, 0, 0, -1]
        if move == 'B_':
            self.currentmove = [0, 0, 0, 0, 0, 1]
        if move == 'y':
            self.currentrotation = -1*(-1)**self.backwards
        if move == 'y_':
            self.currentrotation = 1*(-1)**self.backwards

        self.currentmove = [x*(-1)**self.backwards for x in self.currentmove]

        if back == 0:
            if len(self.movement_list) != 0:
                self.backward_list += [self.movement_list[0]]
                self.movement_list = self.movement_list[1:]
        else:
            if len(self.backward_list) != 0:
                self.movement_list = [
                    self.backward_list[-1]] + self.movement_list
                self.backward_list = self.backward_list[:-1]

    def animation(self):
        if self.currentmove != [0, 0, 0, 0, 0, 0] or self.currentrotation != 0:
            if self.currentangle == 90:
                self.currentangle = 0
                if self.currentmove == [-1, 0, 0, 0, 0, 0]:
                    self.cube3.R(1)
                if self.currentmove == [1, 0, 0, 0, 0, 0]:
                    self.cube3.R_(1)
                if self.currentmove == [0, 1, 0, 0, 0, 0]:
                    self.cube3.L(1)
                if self.currentmove == [0, -1, 0, 0, 0, 0]:
                    self.cube3.L_(1)
                if self.currentmove == [0, 0, -1, 0, 0, 0]:
                    self.cube3.U(1)
                if self.currentmove == [0, 0, 1, 0, 0, 0]:
                    self.cube3.U_(1)
                if self.currentmove == [0, 0, 0, 1, 0, 0]:
                    self.cube3.D(1)
                if self.currentmove == [0, 0, 0, -1, 0, 0]:
                    self.cube3.D_(1)
                if self.currentmove == [0, 0, 0, 0, 1, 0]:
                    self.cube3.F(1)
                if self.currentmove == [0, 0, 0, 0, -1, 0]:
                    self.cube3.F_(1)
                if self.currentmove == [0, 0, 0, 0, 0, -1]:
                    self.cube3.B(1)
                if self.currentmove == [0, 0, 0, 0, 0, 1]:
                    self.cube3.B_(1)
                if self.currentrotation == 1:
                    self.cube3.rotate_left()
                if self.currentrotation == -1:
                    self.cube3.rotate_right()

                self.currentmove = [0, 0, 0, 0, 0, 0]
                self.currentrotation = 0
            else:
                self.currentangle += self.speed
        else:
            if self.single_step == 0:
                if self.backwards == 0 and len(self.movement_list) != 0:
                    self.getmove(0)
                elif self.backwards == 1 and len(self.backward_list) != 0:
                    self.getmove(1)
        self.updateGL()
