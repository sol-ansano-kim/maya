from maya import cmds
from maya import OpenMayaUI
from maya import OpenMaya
import os

## TODO
class View(object):
    def __init__(self):
        super(View, self).__init__()
        self.view = OpenMayaUI.M3dView.active3dView()
        self.camera = OpenMaya.MDagPath()
        self.view.getCamera(self.camera)

    def camera(self):
        if (self.camera.isValid()):
            return self.camera.partialPathName()
        return None

    def size(self):
        return (self.view.portWidth(), self.view.portHeight())


class Camera(object):
    PAN_H = "horizontalPan"
    PAN_V = "verticalPan"
    PAN_ZOOM = "zoom"
    PAN_ENABLE = "panZoomEnabled"
    ASPECT_H = "horizontalFilmAperture"
    ASPECT_V = "verticalFilmAperture"
    IMAGE_H = "sizeX"
    IMAGE_V = "sizeY"
    IMAGE_PATH = "imageName"
    IMAGE_PLANE_TYPE = "imagePlane"
    IMAGE_FIT = "fit"

    def __init__(self, camera_name):
        super(Camera, self).__init__()
        self.image_plane = None
        self.image_path = None
        self.name = camera_name
        self.getImagePlane()

    def __attr(self, attr_name):
        return "%s.%s" % (self.name, attr_name)

    def __isSetable(self, attr):
        if (cmds.listConnections(attr, s=1, d=0) != None):
            cmds.warning("attr has a input connections : %s" % (attr))
            return False
        if (cmds.getAttr(attr, l=1)):
            cmds.warning("attr is locked : %s" % (attr))
            return False
        return True

    def __exists(self, attr_name):
        if (cmds.objExists(self.name) == False):
            cmds.waning("could not find camera : %s" % (self.name))
            return False
        if (cmds.attributeQuery(attr_name, n=self.name, ex=1) == False):
            cmds.warning("could not find the attribute : %s" % (attr_name))
            return False
        return True
    
    def getImagePlane(self):
        cons = cmds.listConnections(self.name, s=1, d=0, 
                                    type=Camera.IMAGE_PLANE_TYPE)
        if cons != None:
            self.image_plane = cons[0]
            img = cmds.getAttr("%s.%s" % (self.image_plane, Camera.IMAGE_PATH))
            if img and os.path.isfile(img):
                self.image_path = img
            else:
                self.image_path = None
        else:
            self.image_plane = None
            self.image_path = None

    def set(self, attr_name, value):
        attr = self.__attr(attr_name)
        if (self.__exists(attr_name) and self.__isSetable(attr)):
            cmds.setAttr(attr, value)

    def get(self, attr_name):
        if (self.__exists(attr_name)):
            return cmds.getAttr(self.__attr(attr_name))
        return None

    def aspectH(self):
        if self.image_plane:
            return cmds.getAttr("%s.%s" % (self.image_plane, Camera.IMAGE_H))
        return self.get(Camera.ASPECT_H)

    def aspectV(self):
        if self.image_plane:
            return cmds.getAttr("%s.%s" % (self.image_plane, Camera.IMAGE_V))
        return self.get(Camera.ASPECT_V)

    def checkPanEnable(self):
        if (self.get(Camera.PAN_ENABLE) == False):
            self.set(Camera.PAN_ENABLE, True)

    def setH(self, value):
        self.checkPanEnable()
        self.set(Camera.PAN_H, value)

    def setV(self, value):
        self.set(Camera.PAN_V, value)

    def setZoom(self, value):
        self.set(Camera.PAN_ZOOM, value)

    def getH(self):
        return self.get(Camera.PAN_H)

    def getV(self):
        return self.get(Camera.PAN_V)

    def getZoom(self):
        return self.get(Camera.PAN_ZOOM)

    def resetPan(self):
        self.setZoom(1.0)
        self.setV(0)
        self.setH(0)
        
    def fitType(self):
        if self.image_plane:
            return cmds.getAttr("%s.%s" % (self.image_plane, Camera.IMAGE_FIT))


def killExistenceWindow(window_name):
    if cmds.window(window_name, q=1, ex=1):
        cmds.deleteUI(window_name)


def getCamera():
    sels = cmds.ls(sl=1)
    if sels:
        obj = sels[0]
        if cmds.objectType(obj) == "transform":
            shapes = cmds.listRelatives(obj, s=1)
            if shapes:
                obj = shapes[0]
        if cmds.objectType(obj) == "camera":
            return obj
    cmds.warning("select a camera")
    return None
