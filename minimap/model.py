from . import mayaFunction as func


class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.view = None
        self.camera = None
        self.reload()

    def reload(self):
        self.view = func.View()
        self.camera = func.Camera(self.view.camera())

    def UI2Pan(self, h, v, z=1):
        self.camera.setH(self.camera.horizonAspect() * h)
        self.camera.setV(self.camera.verticalAspect() * v)

    def pan2UI(self, ui):
        ui.setH(self.camera.getH / self.camera.horizonAspect())
        ui.setV(self.camera.getV / self.camera.verticalAspect())
        