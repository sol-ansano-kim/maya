from . import mayaFunction as func


CAMERA = None
UI = None
DRAW_SCALE = 0.25
FILL_FIT = 0
BEST_FIT = 1
HORIZON_FIT = 2
VERTICAL_FIT = 3
TOSIZE_FIT = 4
ZOOM_MIN = 1
ZOOM_MAX = 200
ZOOM_DEFAULT = 100

def isValid():
    if CAMERA and UI:
        return True
    return False


def setUI(ui):
    global UI
    UI = ui


def getCamera():
    global CAMERA
    cam_name = func.getCamera()
    if cam_name:
        CAMERA = func.Camera(cam_name)
    else:
        CAMERA = None


def getScreenSize(w, h):
    ft = CAMERA.fitType()
    aspect_h = CAMERA.aspectH()
    aspect_v = CAMERA.aspectV()

    if ft == FILL_FIT:
        VERTICAL_FIT if aspect_h < aspect_v else HORIZON_FIT
    elif ft == BEST_FIT:
        VERTICAL_FIT if aspect_h > aspect_v else HORIZON_FIT

    if ft == HORIZON_FIT or ft == TOSIZE_FIT:
        h = int(w / aspect_h * aspect_v)
    elif ft == VERTICAL_FIT or ft == TOSIZE_FIT:
        w = int(h / aspect_v * aspect_h)
    return (w, h)


def UI2Pan(h, v, z):
    if CAMERA and CAMERA.exists():
        CAMERA.setH(h * CAMERA.aspectH())
        CAMERA.setV(v * CAMERA.aspectV() * -1)
        CAMERA.setZoom(z)


def modifyZoom(value):
    if UI:
        UI.zoom_line.setText(str(value))

# def pan2UI(self, ui):
#     UI.setH(CAMERA.getH / CAMERA.aspectH())
#     UI.setV(CAMERA.getV / CAMERA.aspectV())
