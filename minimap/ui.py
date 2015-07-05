from PySide import QtGui
from PySide import QtCore
from maya import OpenMayaUI
import shiboken
from . import function as func


UI_TITLE = "MINIMAP"
UI_OBJECT_NAME = "minimap_maya_camera_navigator"


class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__(wrapQt())
		self.setObjectName(UI_OBJECT_NAME)
		self.setWindowTitle(UI_TITLE)


def wrapQt():
	return shiboken.wrapInstance(OpenMayaUI.MQtUtil_mainWindow(),
		                         QtGui.QMainWindow)


def Show():
	func.killExistenceWindow(UI_OBJECT_NAME)
	window = MainWindow()
	window.show()