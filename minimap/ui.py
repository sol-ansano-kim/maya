from PySide import QtGui
from PySide import QtCore
from maya import OpenMayaUI
import shiboken
from . import mayaFunction as func
from . import model
import os


UI_TITLE = "MINIMAP"
UI_OBJECT_NAME = "minimap_maya_camera_navigator"


class DrawWidget(QtGui.QLabel):
    backgroun_color = QtGui.QColor.fromHsv(0, 0, 20)
    dot_line_pen = QtGui.QPen(QtGui.QColor.fromHsv(0, 0, 200))
    def __init__(self):
        super(DrawWidget, self).__init__()
        self.setObjectName("minimap_draw_widget")
        self.image = None
        self.pushed = False
        self.rect_x = 0
        self.rect_y = 0
        self.rect_w = 10
        self.rect_h = 10
        self.frame_w = 100
        self.frame_h = 100
        self.image_w = 0
        self.image_h = 0
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
        ### rect geometry
        paint.drawRect(*self.__rectGeometry())
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
        posx = self.rect_x - (self.rect_w / 2.0)
        posy = self.rect_y - (self.rect_h / 2.0)
        sizew = self.rect_w if self.rect_w != self.frame_w else self.rect_w - 1
        sizeh = self.rect_h if self.rect_h != self.frame_h else self.rect_h - 1
        return (posx, posy, sizew, sizeh)
        
    def mouseMoveEvent(self, evnt):
        self.update()
        
    def mousePressEvent(self, evnt):
        if (evnt.button() == QtCore.Qt.MouseButton.LeftButton):
            self.pushed = True
        #QtCore.Qt.MouseButton.RightButton
    
    def mouseReleaseEvent(self, evnt):
        self.pushed = False
        
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
        self.update()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(wrapQt())        
        self.image_scale = 0.25
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
        self.draw_widget = DrawWidget()
        main_layout.addWidget(self.draw_widget)
        ### alignment
        main_layout.setAlignment(QtCore.Qt.AlignHCenter)

    def reset(self):
        self.draw_widget.reset()


def wrapQt():
    return shiboken.wrapInstance(OpenMayaUI.MQtUtil_mainWindow(),
                                 QtGui.QMainWindow)


def Create():
    func.killExistenceWindow(UI_OBJECT_NAME)
    return MainWindow()
