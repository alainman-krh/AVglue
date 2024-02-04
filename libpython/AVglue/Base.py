#AVglue/Base.py
#-------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod


#==Signals and traps
#===============================================================================
class Signal():
	def __init__(self, id):
		self.id = id

	def serialize(self):
		return f"SIG {self.id}"


#-------------------------------------------------------------------------------
class SignalTraps():
	def __init__(self, response_map=None):
		if response_map is None:
			response_map = {}
		self.response_map = response_map

	def trap(self, sig:Signal):
		return self.response_map.get(sig.id, None)


#==
#===============================================================================
class OperatingEnvironment():
	"""Will typically have only one. Cleaner than global variables."""
	def __init__(self):
		self.modes = {}
		self.mode_add("OFF", tuple())
		self.mode_setactive("OFF")
		self.state={} #Actions can store data here

	def log_info(self, msg):
		print(msg)

	def log_error(self, msg):
		print(msg)

	def mode_add(self, id, layer_stack):
		self.modes[id] = tuple(layer_stack) #tuples are more efficient

	def mode_setactive(self, id):
		self.mode_activeid = id
		self.mode_activestack = self.modes[id] #Keep it cached (avoid constant lookup)

	def signal_trigger(self, sig:Signal):
		for layer in self.mode_activestack:
			layer:SignalTraps
			action = layer.trap(sig)
			if action is not None:
				action:AbstractAction
				action.run(self)
				return
		self.log_error(f"Signal not trapped: {sig.id}")



#==Abstract bulding blocks
#===============================================================================
class AbstractAction(metaclass=ABCMeta):
	@abstractmethod
	def run(self, env:OperatingEnvironment): #execute?
		return
	@abstractmethod
	def serialize(self):
		return ""
	@staticmethod
	def build_from_strargs(strargs):
		pass
