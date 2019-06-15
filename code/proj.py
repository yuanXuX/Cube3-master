import sys
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import QtOpenGL

import os
import copy

from face_read_v2 import face_read


def give_color():
    img = cv2.imread("capture_python.png")
    return face_read(img)


class ColorBotton(QPushButton):
    def __init__(self, name):
        super().__init__(name)
        self.color = 0


class CheckCube(QWidget):

    def __init__(self):
        super().__init__()
        self.it = 0
        self.is_scan = True  # 用于确认
        # color = {'W':0, 'R':1, 'G':2, 'B':3, 'O':4, 'Y':5, 'U':6}
        self.colors = ['white', 'red', 'green', 'blue', 'orange', 'yellow']
        self.initUI()

    def initButtons(self, names, positions, grid):
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = ColorBotton(name)
            button.clicked.connect(self.buttonClicked)
            button.setStyleSheet(
                'background-color:{};color:{}'.format('white', 'white'))
            menu = QMenu()
            a = self.size()
            button.setFixedSize(a/3)
            grid.addWidget(button, *position)

    def initUI(self):
        self.grid = QGridLayout()
        grid = self.grid
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.operate)  # 计时结束调用operate()方法
        self.timer.start(200)  # 设置计时间隔并启动
        self.setLayout(grid)
        names = ['1', '2', '3',
                 '4', '5', '6',
                 '7', '8', '9']
        positions = [(i, j) for i in range(3) for j in range(3)]
        self.positions = positions
        self.setFixedSize(300, 300)
        self.initButtons(names, positions, grid)
        self.move(300, 150)

    def ret_grid(self):
        return self.grid

    def buttonClicked(self):
        sender = self.sender()
        self.it = (self.it + 1) % 6
        it = self.it
        sender.color = it
        sender.setStyleSheet(
            'background-color:{};color:{}'.format(self.colors[it], self.colors[it]))

    # return the colors of 9 buttons
    def buttonColors(self):
        grid = self.grid
        positions = self.positions
        colors = []
        for i in range(9):
            widget = grid.itemAtPosition(
                positions[i][0], positions[i][1]).widget()
            colors.append(widget.color)

        mat = [colors[0:3], colors[3:6], colors[6:9]]
        mat[0][0], mat[0][2] = mat[0][2], mat[0][0]
        mat[1][0], mat[1][2] = mat[1][2], mat[1][0]
        mat[2][0], mat[2][2] = mat[2][2], mat[2][0]
        return mat

    def operate(self):
        grid = self.grid
        positions = self.positions
        is_scan = self.is_scan
        if (is_scan):
            color = give_color()
            for i in range(9):
                widget = grid.itemAtPosition(
                    positions[i][0], positions[i][1]).widget()
                widget.color = color[i]
                widget.setStyleSheet(
                    'background-color:{};color:{}'.format(self.colors[color[i]], self.colors[color[i]]))


class Ui_MainWindow(QtWidgets.QWidget):
    text = "start"

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()
        self.timer_shot = QtCore.QTimer()
        self.timer_shot.timeout.connect(self.time_shot)
        self.cap = cv2.VideoCapture()
        self.check_color = CheckCube()
        self.check_color2 = CheckCube()
        self.CAM_NUM = 0
        self.set_ui()
        self.slot_init()
        self.__flag_work = 0
        self.x = 0
        self.shot_count = 0
        self.mat = [[], [], [], [], [], []]
        self.face_stored = 0

    def set_ui(self):
        self.__layout_main = QtWidgets.QHBoxLayout()
        self.__layout_fun_button = QtWidgets.QVBoxLayout()
        self.__layout_data_show = QtWidgets.QVBoxLayout()
        self.__layout_gl = QtWidgets.QVBoxLayout()
        self.__layout_gl_button = QtWidgets.QVBoxLayout()
        self.__layout_gl_rotate = QtWidgets.QVBoxLayout()
        self.__layout_gl_rotate_sub = QtWidgets.QHBoxLayout()
        # 摄像头
        self.button_open_camera = QtWidgets.QPushButton(u'打开相机')
        self.button_close = QtWidgets.QPushButton(u'退出')
        self.button_shot = QtWidgets.QPushButton(u'')
        self.button_open_camera.setMinimumHeight(50)
        self.button_close.setMinimumHeight(50)
        self.button_shot.setMinimumHeight(50)
        self.button_close.move(10, 100)
        # 3D Cube
        self.stateButton = QtWidgets.QPushButton(u'播放动画')
        self.Button1 = QtWidgets.QPushButton(u'随机打乱')
        self.Button2 = QtWidgets.QPushButton(u'解出还原步骤')
        self.Button3 = QtWidgets.QPushButton(u'分步详解')    #add
        self.Button4 = QtWidgets.QPushButton(u'观看教程')
        self.picshow = QtWidgets.QGraphicsView()
        self.lastButton = QtWidgets.QPushButton(u'上一步')
        self.nextButton = QtWidgets.QPushButton(u'下一步')
        self.openGLWidget = QtOpenGL.GLDemo(None)
        self.openGLWidget.setMinimumSize(600, 600)
        self.upButton = QtWidgets.QPushButton(u"上")
        self.leftButton = QtWidgets.QPushButton(u"左")
        self.downButton = QtWidgets.QPushButton(u"下")
        self.rightButton = QtWidgets.QPushButton(u"右")
        self.stateButton.clicked.connect(self.changeState)
        self.lastButton.clicked.connect(self.nextStep)
        self.nextButton.clicked.connect(self.lastStep)
        self.Button1.clicked.connect(self.openGLWidget.button_scramble)
        self.Button2.clicked.connect(self.openGLWidget.button_cfop)
        self.Button3.clicked.connect(self.openGLWidget.button_valid)         #add
        self.Button4.clicked.connect(self.toturial)         #add
        self.upButton.clicked.connect(self.openGLWidget.upButton)
        self.leftButton.clicked.connect(self.openGLWidget.leftButton)
        self.downButton.clicked.connect(self.openGLWidget.downButton)
        self.rightButton.clicked.connect(self.openGLWidget.rightButton)
        # 信息显示
        self.label_show_camera = QtWidgets.QLabel()
        self.label_move = QtWidgets.QLabel()
        self.label_move.setFixedSize(200, 200)
        self.label_show_camera.setAutoFillBackground(True)
        self.__layout_gl_button.addWidget(self.Button1)
        self.__layout_gl_button.addWidget(self.Button2) 
        self.__layout_gl_button.addWidget(self.Button3)             #add
        self.__layout_gl_button.addWidget(self.nextButton)
        self.__layout_gl_button.addWidget(self.lastButton)
        self.__layout_gl_button.addWidget(self.stateButton)
        self.__layout_fun_button.addWidget(self.button_open_camera)
        self.__layout_fun_button.addWidget(self.button_shot)
        self.button_shot.hide()
        self.__layout_fun_button.addWidget(self.check_color)
        self.__layout_gl_rotate.addWidget(self.Button4)
        self.__layout_gl_rotate.addWidget(self.upButton)
        self.__layout_gl_rotate_sub.addWidget(self.leftButton)
        self.__layout_gl_rotate_sub.addWidget(self.downButton)
        self.__layout_gl_rotate_sub.addWidget(self.rightButton)
        self.__layout_gl_rotate.addLayout(self.__layout_gl_rotate_sub)
        self.__layout_main.addLayout(self.__layout_fun_button)
        self.__layout_main.addLayout(self.__layout_gl_button)
        self.__layout_main.addWidget(self.openGLWidget)
        self.__layout_main.addWidget(self.picshow)
        self.picshow.hide()
        self.__layout_main.addWidget(self.label_show_camera)
        self.__layout_main.addLayout(self.__layout_gl_rotate)
        self.setLayout(self.__layout_main)
        self.label_move.raise_()
        self.setWindowTitle(u'Cube Solver')

    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        self.button_close.clicked.connect(self.close)
        self.button_shot.clicked.connect(self.shot)

    def faces_remaining(self):
        ret_str = u"剩余:"
        rem = 0
        if self.mat[0] == []:
            ret_str += u"白"
            rem = 1
        if self.mat[1] == []:
            ret_str += u"红"
            rem = 1
        if self.mat[2] == []:
            ret_str += u"绿"
            rem = 1
        if self.mat[3] == []:
            ret_str += u"蓝"
            rem = 1
        if self.mat[4] == []:
            ret_str += u"橙"
            rem = 1
        if self.mat[5] == []:
            ret_str += u"黄"
            rem = 1
        if rem == 0:
            ret_str = u"关闭相机并更新魔方"
        return ret_str

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.timer_shot.start(200)
                self.Button1.hide()
                self.Button2.hide()
                self.Button3.hide()
                self.Button4.hide()
                self.lastButton.hide()
                self.nextButton.hide()
                self.stateButton.hide()
                self.upButton.hide()
                self.leftButton.hide()
                self.downButton.hide()
                self.rightButton.hide()
                self.button_open_camera.setText(self.faces_remaining())
                self.button_shot.setText(u'拍摄本面')
                self.openGLWidget.hide()
                self.button_shot.show()
                msg = QtWidgets.QMessageBox.information(self,"Information","注意：拍摄蓝绿红橙面时黄面在上，拍摄黄白面时橙面在上")
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_camera.clear()
            self.openGLWidget.show()
            self.Button1.show()
            self.Button2.show()
            self.Button3.show()
            self.Button4.show()
            self.lastButton.show()
            self.nextButton.show()
            self.stateButton.show()
            self.upButton.show()
            self.leftButton.show()
            self.downButton.show()
            self.rightButton.show()
            self.button_shot.hide()
            self.button_open_camera.setText(u'打开相机')
            self.face_stored = 0
            for i in self.mat:
                if i != []:
                    self.face_stored += 1
            if self.face_stored == 6:
                self.mat[0][0][0], self.mat[0][0][2] = self.mat[0][0][2], self.mat[0][0][0]
                self.mat[0][1][0], self.mat[0][1][2] = self.mat[0][1][2], self.mat[0][1][0]
                self.mat[0][2][0], self.mat[0][2][2] = self.mat[0][2][2], self.mat[0][2][0]
                self.openGLWidget.cube3.input_raw(self.mat)
                self.mat = [[], [], [], [], [], []]

    def show_camera(self):
        flag, self.image = self.cap.read()
        show = cv2.resize(self.image, (640, 480))
        show = cv2.rectangle(show, (225, 95), (515, 385), (200, 200, 200), 3)
        show = cv2.flip(show, 1)
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(
            show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        if (self.check_color.is_scan):
            self.label_show_camera.setPixmap(
                QtGui.QPixmap.fromImage(showImage))

    def time_shot(self):
        if self.timer_camera.isActive() == False:
            return
        ret, frame = self.cap.read()
        frame = frame[100:380, 230:510]
        frame = cv2.flip(frame, 1)
        face_read(frame)
        cv2.imwrite("capture_python.png", frame)

    def shot(self):
        if self.timer_camera.isActive() == False:
            return
        ret, frame = self.cap.read()
        shot_count = self.shot_count
        self.check_color.is_scan = not self.check_color.is_scan
        shot_count += 1
        if (shot_count == 13):
            shot_count = 1
        self.button_shot.setText(u'修改下方颜色后确认')
        if (shot_count % 2 == 0):
            self.button_shot.setText(u'拍摄本面')
            self.mat[self.check_color.buttonColors()[1][1]] = copy.deepcopy(
                self.check_color.buttonColors())
            self.button_open_camera.setText(self.faces_remaining())
        frame = frame[100:380, 230:510]
        frame = cv2.flip(frame, 1)
        face_read(frame)
        cv2.imwrite("capture_python.png", frame)
        self.shot_count = shot_count

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        if self.timer_camera.isActive():
            self.timer_camera.stop()
        event.accept()

    def response_mat(self):
        if (len(self.mat) == 6):
            return self.mat
        else:
            return []

    def changeState(self):
        _translate = QtCore.QCoreApplication.translate
        if self.openGLWidget.single_step == 1:
            self.openGLWidget.single_step = 0
            self.openGLWidget.backwards = 0
            self.text = "暂停动画"
            self.stateButton.setText(self.text)
        elif self.openGLWidget.single_step == 0:
            self.openGLWidget.single_step = 1
            self.text = "播放动画"
            self.stateButton.setText(self.text)

    def lastStep(self):
        self.openGLWidget.backwards = 0
        self.openGLWidget.getmove(0)

    def nextStep(self):
        self.openGLWidget.backwards = 1
        self.openGLWidget.getmove(1)

    def toturial(self):
        if self.openGLWidget.isVisible():
            self.button_open_camera.hide()
            self.button_shot.hide()
            self.check_color.hide()
            self.Button1.hide()
            self.Button2.hide()
            self.Button3.hide()
            self.lastButton.hide()
            self.nextButton.hide()
            self.stateButton.hide()
            self.upButton.hide()
            self.leftButton.hide()
            self.downButton.hide()
            self.rightButton.hide()
            self.openGLWidget.hide()
            self.picshow.show()
            img=cv2.imread("timg.jpg")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            x = img.shape[1]
            y = img.shape[0]
            self.zoomscale=1
            frame = QImage(img, x, y, QImage.Format_RGB888)
            pix = QPixmap.fromImage(frame)
            self.item=QGraphicsPixmapItem(pix)
            self.scene=QGraphicsScene()
            self.scene.addItem(self.item)
            self.picshow.setScene(self.scene)
            self.Button4.setText(u'返回动画展示')
        else:
            self.button_open_camera.show()
            self.check_color.show()
            self.Button1.show()
            self.Button2.show()
            self.Button3.show()
            self.lastButton.show()
            self.nextButton.show()
            self.stateButton.show()
            self.upButton.show()
            self.leftButton.show()
            self.downButton.show()
            self.rightButton.show()
            self.picshow.hide()
            self.openGLWidget.show()
            self.Button4.setText(u'观看教程')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
