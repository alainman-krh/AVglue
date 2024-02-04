#AVglue/Actions.py
#-------------------------------------------------------------------------------
from .Base import AbstractAction
from os import system
import ctypes


#==Concrete Actions
#===============================================================================
class Action_TriggerLocalSignal(AbstractAction):
	"""Trigger a signal that gets processed locally"""
	def __init__(self, signame):
		self.signame = signame

	def serialize(self):
		return f"TRIGLCL {self.signame}"

class Action_TriggerComSignal(AbstractAction):
	"""Trigger a signal that gets sent through a com device"""
	def __init__(self, signame):
		self.signame = signame

	def serialize(self):
		return f"TRIGCOM {self.signame}"

class Action_SendKeys(AbstractAction):
	"""Sends a key sequence"""
	#TODO: Send to a particular application???
	def __init__(self, wnd, seq):
		"""-wnd=0 sends key sequence to active window"""
		self.wnd = wnd
		self.seq = seq

	def run(self):
		print("Sending:", self.seq)
		result = ctypes.windll.user32.SendInput(self.seq)
		return result

	def serialize(self):
		return f"SENDKEYS {self.wnd} {self.seq}"

class Action_ExecuteShell(AbstractAction):
	"""Execute shell - not necessarily portable"""
	def __init__(self, cmd):
		self.cmd = cmd

	def run(self):
		system(self.cmd)

	def serialize(self):
		return f"EXECSHELL {self.cmd}"

class Action_ExecuteCustomPy(AbstractAction):
	"""Execute custom python function (by name/function id)"""
	def __init__(self, fnid):
		self.fnid = fnid

	def serialize(self):
		return f"EXECPY {self.fnid}"

class Action_ExecuteSequence(AbstractAction):
	"""Sequential list of actions"""
	def __init__(self, action_list):
		self.action_list = action_list #::AbstractAction[]

	def run(self):
		for action in self.action_list:
			action.run()
