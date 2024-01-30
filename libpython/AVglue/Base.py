#AVglue/Base.py
from abc import ABCMeta, abstractmethod


#==Actions
#===============================================================================
class AbstractSignal(metaclass=ABCMeta):
	def __init__(self, trigger):
		self.trigger = trigger #Either Signal or Task

class VirtualSignal(AbstractSignal):
	pass

class PhysicalSignal(AbstractSignal):
	pass

class CommSignal(AbstractSignal):
	"""Relay signal on """
	pass


#==Actions
#===============================================================================
class AbstractAction(metaclass=ABCMeta):
	pass

class Action_SendKey(AbstractAction):
	pass

class Action_TriggerVirtualSignal(AbstractAction):
	pass

class Action_TriggerComSignal(AbstractAction):
	"""Trigger a signal that gets sent through a com device"""
	pass

class Action_ExecuteShell(AbstractAction):
	#TODO: Different types of execute?
	pass

class Action_ExecuteTask(AbstractAction):
	#TODO: Different types of execute?
	pass


#==Task
#===============================================================================
class Task():
	def __init__(self, action_list):
		pass