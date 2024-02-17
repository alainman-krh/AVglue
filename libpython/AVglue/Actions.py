#AVglue/Actions.py: Platform-independent AVglue actions
#-------------------------------------------------------------------------------
from .Base import *
from time import sleep
from os import system #Handled by python in platform-independent fashion


#==Concrete Actions
#===============================================================================
class Action_TriggerLocal(AbstractAction):
	"""Trigger a signal that gets processed locally"""
	def __init__(self, sig:Signal, data_int64=None):
		self.sig = sig
		self.data_int64 = data_int64
	def run(self, env:OperatingEnvironment):
		return env.signal_trigger(self.sig, data_int64=self.data_int64)
	def serialize(self):
		return f'TRIGLCL "{self.sig.serialize()}"'

#-------------------------------------------------------------------------------
class Action_TriggerComSignal(AbstractAction):
	"""Trigger a signal that gets sent through a com device"""
	def __init__(self, sig:Signal, data_int64=None):
		self.sig = sig
		self.data_int64 = data_int64
	def run(self, env:OperatingEnvironment):
		return True #TODO
	def serialize(self):
		return f'TRIGCOM "{self.sig.serialize()}"'

#-------------------------------------------------------------------------------
class Action_Wait(AbstractAction):
	"""Wait for a specified amount of time"""
	def __init__(self, twait=0):
		self.twait = twait
	def run(self, env:OperatingEnvironment):
		sleep(self.twait)
		return True
	def serialize(self):
		return f"WAIT {self.twait}"

#-------------------------------------------------------------------------------
class Action_LogString(AbstractAction):
	"""Log a pre-determined string value"""
	def __init__(self, logstr):
		self.logstr = logstr
	def run(self, env:OperatingEnvironment):
		print(self.logstr)
		return True
	def serialize(self):
		return f"LOGSTR {self.logstr}"

#-------------------------------------------------------------------------------
class Action_DecodeInt64(AbstractAction):
	"""Decode `env.data_int64` using Decoder_Int64 (pattern match)"""
	def __init__(self, decoder_id):
		self.decoder_id = decoder_id
	def run(self, env:OperatingEnvironment):
		#env.log_info(f"Decoding with {self.decoder_id}")
		data = env.data_int64
		decoder = env.decoders_int64.get(self.decoder_id, None)
		if decoder is None:
			env.log_error(f"Decoder not found: {self.decoder_id}")
			return False #Fail
		action = decoder.decode(data) #Might be None... and so try
		if action is None:
			return False #Fail
		return action.run(env)
	def serialize(self):
		return f"DECODEINT64 {self.decoder_id}"

#-------------------------------------------------------------------------------
class Action_SwitchMode(AbstractAction):
	"""Switch operating mode"""
	def __init__(self, modeid):
		self.modeid = modeid
	def run(self, env:OperatingEnvironment):
		env.mode_setactive(self.modeid)
		return True
	def serialize(self):
		return f"SETMODE {self.modeid}"

#-------------------------------------------------------------------------------
class Action_ExecuteShell(AbstractAction):
	"""Execute shell - not necessarily portable"""
	def __init__(self, cmd):
		self.cmd = cmd
	def run(self, env:OperatingEnvironment):
		system(self.cmd)
		return True
	def serialize(self):
		return f"EXECSHELL {self.cmd}"

#-------------------------------------------------------------------------------
class Action_ExecuteCustomPy(AbstractAction):
	"""Execute custom python function (by name/function id)"""
	def __init__(self, fn, fnid=None):
		self.fn = fn
		if fnid is None:
			fnid = fn.__name__
		self.fnid = fnid
	def run(self, env:OperatingEnvironment):
		return self.fn(env)
	def serialize(self):
		return f"EXECPY {self.fnid}"

#-------------------------------------------------------------------------------
class Action_ExecuteSequence(AbstractAction):
	"""Sequential list of actions"""
	def __init__(self, id, action_list):
		self.id = id
		self.action_list = action_list #::AbstractAction[]

	def run(self, env:OperatingEnvironment):
		success = True
		for action in self.action_list:
			success &= action.run(env)
		return success

	def serialize(self):
		return f"EXECSEQ {self.id}"