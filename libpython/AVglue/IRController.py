#AVglue/IRController.py
#-------------------------------------------------------------------------------
from .Base import Signal, OperatingEnvironment
from serial import Serial
import toml


#==ControllerDef
#===============================================================================
class ControllerDef:
	"""Controller definition"""
	def __init__(self):
		self.map = {}
		self.devid = None #Device ID. Typically sereial number of serial device
		pass

	def btnlist_capture(self, siglbl_ordmap, env:OperatingEnvironment, com:Serial):
		for (sig, lbl) in siglbl_ordmap.items():
			print(f"Press button: {lbl}.")
			msg = com.readline()
			(sig, data) = env.message_tosignal(msg)
			if sig is None:
				env.log_error("Error trying to capture IR signal.")
				continue
			self.map[data] = sig
		return

	def write(self, filepath):
		toml.dump(self.map, filepath)

