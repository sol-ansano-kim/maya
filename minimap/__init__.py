from . import model
from . import ui


def Run():
    model.getCamera()
    model.UI = ui.Create()
    if model.isValid():
        model.UI.reset()
        model.UI.show()
