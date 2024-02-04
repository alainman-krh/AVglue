#AVglue/Windows/Actions.py: Windows integrations
#-------------------------------------------------------------------------------
from AVglue.Base import OperatingEnvironment, AbstractAction
import win32com.client as COM
from time import sleep


#==Concrete Actions
#===============================================================================

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
