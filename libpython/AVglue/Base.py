#AVglue/Base.py
#-------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod


#==
#===============================================================================
class OperatingEnvironment():
	"""Will typically have only one. Cleaner than global variables."""
	def __init__(self):
		self.modes = {}
		self.mode_add("OFF", tuple())
		self.mode_setactive("OFF")
	
	def mode_add(self, id, layer_stack):
		self.modes[id] = tuple(layer_stack) #tuples are more efficient

	def mode_setactive(self, id):
		self.mode_activeid = id
		self.mode_activestack = self.modes[id] #Keep it cached (avoid constant lookup)


#==Abstract bulding blocks
#===============================================================================
class AbstractAction(metaclass=ABCMeta):
	@abstractmethod
	def run(self, env:OperatingEnvironment): #execute?
		return
	@abstractmethod
	def serialize(self):
		return ""


#==Main signal class
#===============================================================================
class Signal():
	def __init__(self, id):
		self.id = id

	def serialize(self):
		return f"SIG {self.id}"
