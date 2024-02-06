#AVglue/Windows/Actions.py: Windows integrations
#-------------------------------------------------------------------------------
from AVglue.Base import OperatingEnvironment, AbstractAction
from pycaw.pycaw import IAudioEndpointVolume
from time import sleep
import win32com.client as COM


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
		self.shell = COM.Dispatch("WScript.Shell")

	def run(self, env:OperatingEnvironment):
		if self.appname not in (0, None, "0"):
			self.shell.AppActivate(self.appname)
		if self.twait > 0:
			sleep(self.twait)
		env.log_info(f"Sending: `{self.seq}`")
		self.shell.SendKeys(self.seq)
		return True #success

	def serialize(self):
		return f"SENDKEYS {self.appname} {self.seq} {self.twait}"

#-------------------------------------------------------------------------------
class Action_VolumeSet(AbstractAction):
	"""Sets channel volume to a specific value"""
	def __init__(self, chanid, level_dB):
		self.chanid = chanid
		self.level_dB = level_dB
	def run(self, env:OperatingEnvironment):
		if "MASTER" == self.chanid:
			volume:IAudioEndpointVolume = env.state["WINAUDIO:VOLUME"]
			volume.SetMasterVolumeLevel(self.level_dB, None)
		else:
			env.log_info(f"Channel ID not supported: {self.chanid}")
			return False #Fail
		return True
	def serialize(self):
		return f"VOLSET {self.chanid} {self.level_dB}"

#-------------------------------------------------------------------------------
class Action_VolumeUp(AbstractAction):
	"""Step up channel volume"""
	def __init__(self, chanid):
		self.chanid = chanid
	def run(self, env:OperatingEnvironment):
		if "MASTER" == self.chanid:
			volume:IAudioEndpointVolume = env.state["WINAUDIO:VOLUME"]
			volume.VolumeStepUp(None)
		else:
			env.log_info(f"Channel ID not supported: {self.chanid}")
			return False #Fail
		return True
	def serialize(self):
		return f"VOLUP {self.chanid}"

#-------------------------------------------------------------------------------
class Action_VolumeDn(AbstractAction):
	"""Step down channel volume"""
	def __init__(self, chanid):
		self.chanid = chanid
	def run(self, env:OperatingEnvironment):
		if "MASTER" == self.chanid:
			volume:IAudioEndpointVolume = env.state["WINAUDIO:VOLUME"]
			volume.VolumeStepDown(None)
		else:
			env.log_info(f"Channel ID not supported: {self.chanid}")
			return False #Fail
		return True
	def serialize(self):
		return f"VOLDN {self.chanid}"
