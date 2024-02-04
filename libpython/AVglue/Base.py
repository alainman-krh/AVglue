#AVglue/Base.py
#-------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod


#==Abstract bulding blocks
#===============================================================================
class AbstractAction(metaclass=ABCMeta):
	#@abstractmethod
	def run(self): #execute?
		return
	#@abstractmethod
	def serialize(self):
		return ""


#==Main signal class
#===============================================================================
class Signal():
	def __init__(self, id):
		self.id = id

	def serialize(self):
		return f"SIG {self.id}"
