#AVglue/Base.py
#-------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod
from datetime import datetime


#==Constants
#===============================================================================
FMT_TIMESTAMP = r"%Y-%m-%dT%H:%M:%S"
FMT_TIMESTAMP_FILE = r"%Y%m%d_%Hh%Mm%Ss"
MASK_INT64 = 0xFFFFFFFFFFFFFFFF #64-bit/16 nibbles


#==Helper functions
#===============================================================================
def int64str(v):
	return f"{v:016X}"

def get_timestamp(t=None, fmt=None):
	if t is None:
		t = datetime.now()
	if fmt is None:
		fmt = FMT_TIMESTAMP
	return t.strftime(fmt)

def get_timestamp_file(t=None):
	return get_timestamp(t, fmt=FMT_TIMESTAMP_FILE)


#==General controller/worker classes (ex: for client-server applications)
#===============================================================================
class AbstractController(metaclass=ABCMeta):
	"""Mostly used to identify class as a controller (client side)"""
	pass

class AbstractWorker(metaclass=ABCMeta):
	"""Mostly used to identify class as a worker (listener/server side)"""
	pass


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
	def display(self):
		for (k, v) in self.response_map.items():
			print(f"{k}: {v}")

#-------------------------------------------------------------------------------
class Decoder_Int64():
	def __init__(self, response_map=None):
		if response_map is None:
			response_map = []
		self.response_map = response_map
	
	def add(self, pat, action, mask=None):
		if mask is None:
			mask = MASK_INT64
		_pack = (action, pat, mask) #Create tuple
		self.response_map.append(_pack)

	def decode(self, env, data):
		if data is None:
			if env.verbose:
				env.log_error("WARN: No data to be decoded")
			return None
		for (action, pat, mask) in self.response_map:
			if (data & mask) == pat:
				action:AbstractAction
				#print(action.serialize())
				return action
		if env.verbose:
			env.log_error(f"WARN: No mapping found for data={data:02X}")	
		return None

	def display(self):
		for (action, pat, mask) in self.response_map:
			action:AbstractAction
			astr = action.serialize()

			print(f'{int64str(pat)}, mask={int64str(mask)} -> "{astr}"')


#==OperatingEnvironment
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

#-------------------------------------------------------------------------------
	def signal_trigger(self, sig:Signal, data_int64=None):
		for layer in self.mode_activestack:
			layer:SignalTraps
			action = layer.trap(sig)
			if action is not None:
				action:AbstractAction
				self.data_int64 = data_int64
				if self.verbose:
					self.log_info(f"Triggering: ({sig.serialize()}, 0x{data_int64:02X}).")
				#self.log_info("Running " + action.serialize())
				return action.run(self)
		self.log_info(f'Signal not trapped: "{sig.serialize()}"')
		return False #fail

#-------------------------------------------------------------------------------
	@staticmethod
	def _datastr_toint64(dstr:str):
		try:
			if "0x" == dstr[:2]:
				data = int(dstr, 16)
			else:
				data = int(dstr)
		except:
			data = 0 #Don't crash
		return data

#-------------------------------------------------------------------------------
	def message_tosignal(self, msg:str):
		RESULT_NOSIG = (None, 0)
		tokens = msg.split()
		N = len(tokens)
		if N < 1:
			return RESULT_NOSIG
		elif N > 2:
			self.log_error(f"Only supports signals with up to 1 optional argument:\n`{msg}`")
			return RESULT_NOSIG

		data = None
		if N > 1: #We have data
			data = self._datastr_toint64(tokens[1])

		id = tokens[0]
		return (Signal(id), data)

#-------------------------------------------------------------------------------
	def message_process(self, msg:str):
		(sig, data) = self.message_tosignal(msg)
		if sig is None:
			return False
		return self.signal_trigger(sig, data_int64=data)


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
