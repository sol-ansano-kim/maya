from . import mayaFunction as func


CAMERA = None
UI = None
DRAW_SCALE = 0.125
HORIZON_FIT = 2
VERTICAL_FIT = 3


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

def getScreenSize(w, h):
    ft = CAMERA.fitType()
    ### only support horizon, vertical fit, currently 
    if ft == HORIZON_FIT:
        h = int(w / CAMERA.aspectH() * CAMERA.aspectV())
    else:
        w = int(h / CAMERA.aspectV() * CAMERA.aspectH())
    return (w, h)
    

def UI2Pan(h, v, z):
    if CAMERA and CAMERA.exists():
        CAMERA.setH(h * CAMERA.aspectH())
        CAMERA.setV(v * CAMERA.aspectV() * -1)
        CAMERA.setZoom(z)
    

# def pan2UI(self, ui):
#     UI.setH(CAMERA.getH / CAMERA.aspectH())
#     UI.setV(CAMERA.getV / CAMERA.aspectV())
