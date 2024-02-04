#AVglue/Windows/Actions.py: Windows integrations
#-------------------------------------------------------------------------------
from AVglue.Base import OperatingEnvironment, AbstractAction
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
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

	def serialize(self):
		return f"SENDKEYS {self.appname} {self.seq} {self.twait}"

#-------------------------------------------------------------------------------
class Action_SetVolume(AbstractAction):
	"""Sets master volume to a specific value"""
	#TODO: Send to a particular application???
	def __init__(self, chanid, level_dB):
		self.chanid = chanid
		self.level_dB = level_dB
		devices = AudioUtilities.GetSpeakers()
		interface = devices.Activate(
			IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
		self.volume = cast(interface, POINTER(IAudioEndpointVolume))

	def run(self, env:OperatingEnvironment):
		if "MASTER" == self.chanid:
			self.volume.SetMasterVolumeLevel(self.level_dB, None)
		else:
			env.log_info(f"Channel ID not supported: {self.chanid}")

	def serialize(self):
		return f"SETVOL {self.chanid} {self.level_dB}"
