#AVglue/Actions.py
#-------------------------------------------------------------------------------
from .Base import Signal, OperatingEnvironment, AbstractAction
from time import sleep
from os import system
import win32com.client as COM


#==Concrete Actions
#===============================================================================
class Action_TriggerLocalSignal(AbstractAction):
	"""Trigger a signal that gets processed locally"""
	def __init__(self, signame):
		self.signame = signame
	def run(self, env:OperatingEnvironment):
		env.signal_trigger(Signal(self.signame))
	def serialize(self):
		return f"TRIGLCL {self.signame}"

#-------------------------------------------------------------------------------
class Action_TriggerComSignal(AbstractAction):
	"""Trigger a signal that gets sent through a com device"""
	def __init__(self, signame):
		self.signame = signame
	def run(self, env:OperatingEnvironment):
		return #TODO
	def serialize(self):
		return f"TRIGCOM {self.signame}"

#-------------------------------------------------------------------------------
class Action_Wait(AbstractAction):
	"""Wait for a specified amount of time"""
	def __init__(self, twait=0):
		self.twait = twait
	def run(self, env:OperatingEnvironment):
		sleep(self.twait)
	def serialize(self):
		return f"WAIT {self.twait}"

#-------------------------------------------------------------------------------
class Action_SendKeys(AbstractAction):
	"""Sends a key sequence"""
	#TODO: Send to a particular application???
	def __init__(self, appname, seq, twait=0):
		"""-appname=0 sends key sequence to active window"""
		self.appname = appname
		self.seq = seq
		self.twait = twait

	def run(self, env:OperatingEnvironment):
		shell = COM.Dispatch("WScript.Shell")
		if self.appname not in (0, None, "0"):
			shell.AppActivate("Calculator")
			if self.twait > 0:
				sleep(self.twait)
		print("Sending:", self.seq)
		shell.SendKeys(self.seq)

	def serialize(self):
		return f"SENDKEYS {self.appname}, {self.seq}, {self.twait}"

#-------------------------------------------------------------------------------
class Action_LogString(AbstractAction):
	"""Log a pre-determined string value"""
	def __init__(self, logstr):
		self.logstr = logstr
	def run(self, env:OperatingEnvironment):
		print(self.logstr)
	def serialize(self):
		return f"LOGSTR {self.logstr}"

#-------------------------------------------------------------------------------
class Action_ExecuteShell(AbstractAction):
	"""Execute shell - not necessarily portable"""
	def __init__(self, cmd):
		self.cmd = cmd
	def run(self, env:OperatingEnvironment):
		system(self.cmd)
	def serialize(self):
		return f"EXECSHELL {self.cmd}"

#-------------------------------------------------------------------------------
class Action_ExecuteCustomPy(AbstractAction):
	"""Execute custom python function (by name/function id)"""
	def __init__(self, fnid):
		self.fnid = fnid
	def run(self, env:OperatingEnvironment):
		return #TODO
	def serialize(self):
		return f"EXECPY {self.fnid}"

#-------------------------------------------------------------------------------
class Action_ExecuteSequence(AbstractAction):
	"""Sequential list of actions"""
	def __init__(self, id, action_list):
		self.id = id
		self.action_list = action_list #::AbstractAction[]

	def run(self, env:OperatingEnvironment):
		for action in self.action_list:
			action.run(env)

	def serialize(self):
		return f"EXECSEQ {self.id}"