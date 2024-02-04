#AVglue/Actions.py
#-------------------------------------------------------------------------------
from .Base import AbstractAction
from os import system


#==Concrete Actions
#===============================================================================
class Action_TriggerLocalSignal(AbstractAction):
	"""Trigger a signal that gets processed locally"""
	def __init__(self, sigid):
		self.sigid = sigid

	def serialize(self):
		return f"TRIGLCL {self.sigid}"

class Action_TriggerComSignal(AbstractAction):
	"""Trigger a signal that gets sent through a com device"""
	def __init__(self, sigid):
		self.sigid = sigid

	def serialize(self):
		return f"TRIGCOM {self.sigid}"

class Action_SendKey(AbstractAction):
	pass

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
