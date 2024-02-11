#AVglue/Base.py
#-------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod

#==Constants
#===============================================================================
MASK_INT64 = 0xFFFFFFFFFFFFFFFF #64-bit/16 nibbles


#==Helper functions
#===============================================================================
def int64str(v):
	return f"{v:016X}"


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

#-------------------------------------------------------------------------------
class Decoder_Int64():
	def __init__(self, response_map=None):
		if response_map is None:
			response_map = []
		self.response_map = response_map
	
	def add(self, action, pat, mask=None):
		if mask is None:
			mask = MASK_INT64
		_pack = (action, pat, mask) #Create tuple
		self.response_map.append(_pack)

	def decode(self, data):
		if data is None:
			print("WARN: No data to be decoded")
			return None
		for (action, pat, mask) in self.response_map:
			if (data & mask) == pat:
				action:AbstractAction
				#print(action.serialize())
				return action
		print("WARN: No mapping found")	
		return None

	def display(self):
		for (action, pat, mask) in self.response_map:
			action:AbstractAction
			astr = action.serialize()

			print(f'"{astr}", {int64str(pat)}, mask={int64str(mask)}')


#==
#===============================================================================
class OperatingEnvironment():
	"""Will typically have only one. Cleaner than global variables."""
	def __init__(self):
		self.verbose = False
		self.modes = {}
		self.actions = {}
		self.mode_add("OFF", tuple())
		self.mode_setactive("OFF")
		self.state={} #Actions can store data here
		self.data_int64 = None
		self.decoders_int64 = {} #Registered Decoder_Int64 objects

	def log_info(self, msg):
		print(msg)

	def log_error(self, msg):
		print(msg)

	def mode_add(self, id, layer_stack):
		self.modes[id] = tuple(layer_stack) #tuples are more efficient

	def mode_setactive(self, id):
		self.mode_activeid = id
		self.mode_activestack = self.modes[id] #Keep it cached (avoid constant lookup)
		if self.verbose:
			self.log_info("Switching to mode: " + id)

	def actions_add(self, id, action):
		self.actions[id] = action #:AbstractAction

	def decoders_add(self, id, decoder:Decoder_Int64):
		#Assumes always Int64 for the time being.
		self.decoders_int64[id] = decoder

	def signal_trigger(self, sig:Signal):
		for layer in self.mode_activestack:
			layer:SignalTraps
			action = layer.trap(sig)
			if action is not None:
				action:AbstractAction
				#self.log_info("Running " + action.serialize())
				return action.run(self)
		self.log_info(f'Signal not trapped: "{sig.serialize()}"')
		return False #fail



#==Abstract bulding blocks
#===============================================================================
class AbstractAction(metaclass=ABCMeta):
	@abstractmethod
	def run(self, env:OperatingEnvironment): #execute?
		return True #Return success?
	@abstractmethod
	def serialize(self):
		return ""
	@staticmethod
	def build_from_strargs(strargs):
		pass
