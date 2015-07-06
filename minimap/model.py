from . import function as func


class Model(object):	
	def __init__(self):
		super(Model, self).__init__()
		self.view = None
		self.camera = None
		self.reload()
		
	def reload(self):
		self.view = func.View()
		self.camera = func.Camera(self.view.camera())
		