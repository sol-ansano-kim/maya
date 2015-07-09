from PySide import QtGui
from PySide import QtCore
from maya import OpenMayaUI
import shiboken
from . import mayaFunction as func
from . import model
import os
import re

RE_NUMBER = re.compile("^[0-9.]+$")
UI_TITLE = "MINIMAP"
UI_OBJECT_NAME = "minimap_maya_camera_navigator"


class DrawWidget(QtGui.QLabel):
    backgroun_color = QtGui.QColor.fromHsv(0, 0, 20)
    dot_line_pen = QtGui.QPen(QtGui.QColor.fromHsv(0, 0, 200))
    def __init__(self):
        super(DrawWidget, self).__init__()
        self.setObjectName("minimap_draw_widget")
        self.image = None
        self.left_pushed = False
        self.right_pushed = False
        self.old_pos = None
        self.rect_x = 0
        self.rect_y = 0
        self.rect_w = 10
        self.rect_h = 10
        self.frame_w = 100
        self.frame_h = 100
        self.image_w = 0
        self.image_h = 0
        self.zoom = 1
        self.clear()

    def paintEvent(self, evnt):
        paint = QtGui.QPainter()
        paint.begin(self)
        ### set black
        paint.fillRect(0, 0, self.frame_w, self.frame_h, self.backgroun_color)
        ### set image
        if self.image:
            paint.drawImage(self.__imageGeometry(), self.image)
        ### draw rect
        paint.setPen(self.dot_line_pen)
        ### draw rect
        paint.drawRect(*self.__rectGeometry())
        ### draw line
        paint.drawLine(self.rect_x - 5, self.rect_y,
                       self.rect_x + 5, self.rect_y)
        paint.drawLine(self.rect_x, self.rect_y - 5,
                       self.rect_x, self.rect_y + 5)
        model.UI2Pan((self.rect_x - self.rect_w / 2.0) / self.rect_w,
                     (self.rect_y - self.rect_h / 2.0) / self.rect_h,
                     self.zoom)
        paint.end()

    def __imageGeometry(self):
        x = 0
        y = 0
        if self.frame_w != self.image_w:
            x = int((self.frame_w - self.image_w) / 2.0)
        if self.frame_h != self.image_h:
            y = int((self.frame_h - self.image_h) / 2.0)
        return QtCore.QRect(x, y, self.image_w, self.image_h)

    def __rectGeometry(self):
        ### position
        posx = self.rect_x - (self.rect_w / 2.0 * self.zoom)
        posy = self.rect_y - (self.rect_h / 2.0 * self.zoom)
        ### rect size
        w = self.rect_w * self.zoom
        h = self.rect_h * self.zoom
        ### if frame size and rect size are same then minus 1 pixel
        sizew = w if abs(w - self.frame_w) > 0.1 else w - 1
        sizeh = h if abs(h - self.frame_h) > 0.1 else h - 1
        return (posx, posy, sizew, sizeh)

    def mouseMoveEvent(self, evnt):
        if self.left_pushed:
            self.__moveRect(evnt)
        elif self.right_pushed:
            if self.old_pos:
                self.__scaleRect(evnt)
            self.old_pos = evnt.pos()

    def __scaleRect(self, evnt):
        moved = evnt.pos() - self.old_pos
        self.old_pos = evnt.pos()
        zoom = self.zoom + (moved.x() + moved.y()) * 0.001
        zoom = zoom if zoom > 0 else 0.001
        model.modifyZoom(zoom)
        self.setZoom(zoom)

    def __moveRect(self, evnt):
        pos = evnt.pos()
        self.rect_x = pos.x()
        self.rect_y = pos.y()
        self.update()

    def mousePressEvent(self, evnt):
        if (evnt.button() == QtCore.Qt.MouseButton.LeftButton):
            self.left_pushed = True
            self.__moveRect(evnt)
        if (evnt.button() == QtCore.Qt.MouseButton.RightButton):
            self.right_pushed = True

    def mouseReleaseEvent(self, evnt):
        self.left_pushed = False
        self.right_pushed = False
        self.old_pos = None


    def __setSize(self):
        self.setFixedSize(self.frame_w, self.frame_h)

    def clear(self):
        self.setImage(None, 100, 100)

    def reset(self):
        path = model.CAMERA.image_path
        img_obj = None
        w = 100
        h = 100
        if path:
            ori_img = QtGui.QImage(path)
            size = ori_img.size()
            ## image size
            self.image_w = int(size.width() * model.DRAW_SCALE)
            self.image_h = int(size.height() * model.DRAW_SCALE)
            img_obj = ori_img.scaled(self.image_w, self.image_h)
            (w, h) = model.getScreenSize(self.image_w, self.image_h)
        self.setImage(img_obj, w, h)

    def setImage(self, image_obj, w, h):
        self.image = image_obj
        self.rect_x = w / 2.0
        self.rect_y = h / 2.0
        self.rect_w = w
        self.rect_h = h
        self.frame_w = w
        self.frame_h = h
        self.__setSize()
        self.zoom = 1
        self.update()

    def getZoom(self):
        return self.zoom

    def setZoom(self, zoom):
        self.zoom = zoom
        self.update()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(wrapQt())
        self.setObjectName(UI_OBJECT_NAME)
        self.setWindowTitle(UI_TITLE)
        self.__makeWidgets()

    def __makeWidgets(self):
        ### central widget, main layout
        central_widget = QtGui.QWidget()
        main_layout = QtGui.QVBoxLayout()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)
        ### draw widget
        draw_layout = QtGui.QHBoxLayout()
        draw_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.draw_widget = DrawWidget()
        draw_layout.addWidget(self.draw_widget)
        main_layout.addLayout(draw_layout)
        ### zoom widget
        zoom_layout = QtGui.QHBoxLayout()
        self.zoom_line = QtGui.QLineEdit("1.0")
        self.zoom_line.setFixedWidth(40)
        reset_button = QtGui.QPushButton("reset")
        zoom_layout.addWidget(self.zoom_line)
        zoom_layout.addWidget(reset_button)
        main_layout.addLayout(zoom_layout)
        ### button layout
        button_layout = QtGui.QHBoxLayout()

        size_1_2 = QtGui.QRadioButton("1/2")
        size_1_4 = QtGui.QRadioButton("1/4")
        size_1_8 = QtGui.QRadioButton("1/8")
        size_1_4.setChecked(True)

        button_layout.addWidget(size_1_2)
        button_layout.addWidget(size_1_4)
        button_layout.addWidget(size_1_8)
        main_layout.addLayout(button_layout)
        ### signal
        self.zoom_line.textEdited.connect(self.slotZoomChanged)
        reset_button.clicked.connect(self.reset)
        size_1_2.clicked.connect(self.toggle_1_2)
        size_1_8.clicked.connect(self.toggle_1_8)
        size_1_4.clicked.connect(self.toggle_1_4)

    def slotZoomChanged(self):
        txt = self.zoom_line.text()
        if RE_NUMBER.match(txt):
            value = float(txt)
            value = value if value > 0 else 0.001
            self.setZoom(value)
            # a = 100 - value  # b = value / a  # c = a * 0.01
            # d = b * c  # e = c * 2 # print d + e

    def toggle_1_4(self):
        model.DRAW_SCALE = 0.25

    def toggle_1_8(self):
        model.DRAW_SCALE = 0.125

    def toggle_1_2(self):
        model.DRAW_SCALE = 0.5

    def reset(self):
        self.zoom_line.setText("1.0")
        self.draw_widget.reset()

    def setZoom(self, value):
        self.draw_widget.setZoom(value)

    def closeEvent(self, evnt):
        model.UI2Pan(0, 0, 1)
        super(QtGui.QMainWindow, self).closeEvent(evnt)


def wrapQt():
    parent = None
    try:
        parent = shiboken.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()),
                                       QtGui.QWidget)
    except:
        pass
    ### i don`t like this way..
    if parent == None:
        RE_MAIN = re.compile("Autodesk Maya.*")
        for wid in QtGui.QApplication.topLevelWidgets():
            name = wid.windowTitle()
            if RE_MAIN.match(name):
                parent = wid
                break
    return parent


def Create():
    func.killExistenceWindow(UI_OBJECT_NAME)
    return MainWindow()
