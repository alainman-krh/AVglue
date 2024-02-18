#AVglue/IRController.py
#-------------------------------------------------------------------------------
from .Base import Signal, OperatingEnvironment
from serial import Serial
from time import time as time_now
import toml


def _IRdata_tostr(data):
	return f"0x{data:02X}"


#==ControllerDef
#===============================================================================
class ControllerDef:
	"""Controller definition"""

	def __init__(self):
		self.map = {}
		self.devid = None #Device ID. Typically sereial number of serial device
		self.siglast_data = 0
		self.siglast_timestamp = time_now()
		self.siglast_timeout = 2
		pass

#-------------------------------------------------------------------------------
	def map_asstring(self):
		return {signame: _IRdata_tostr(data) for (signame, data) in self.map.items()}

	def map_display(self):
		strmap = self.map_asstring()
		for (signame, datastr) in strmap.items():
			print(f"{signame} {datastr}")

#-------------------------------------------------------------------------------
	def write(self, filepath, silent=False):
		"""Write controller definition to file"""
		strmap = self.map_asstring() #Needs data as string
		with open(filepath, "w") as ostrm:
			toml.dump(strmap, ostrm)
		if not silent:
			print("Controller definition written to:\n    " + filepath)

#-------------------------------------------------------------------------------
	def btn_updatemap(self, signame, data):
		self.siglast_timestamp = time_now()
		self.map[signame] = data
		self.siglast_data = data

	def btn_isnew(self, sigdata):
		if time_now() - self.siglast_timestamp > self.siglast_timeout:
			return True
		if sigdata == self.siglast_data:
			return False
		return True

#-------------------------------------------------------------------------------
	def btnlist_capture(self, siglbl_ordmap, env:OperatingEnvironment, com:Serial):
		for (signame, lbl) in siglbl_ordmap.items():
			print(f"Press button: {lbl}.")
			detected = False
			while not detected:
				msg = com.readline().decode("utf-8")
				(sig, data) = env.message_tosignal(msg)
				if sig is None:
					env.log_error("--->Error trying to capture IR signal.")
					continue

				signame_in = sig.id
				if "IR" == signame_in:
					if self.btn_isnew(data):
						self.btn_updatemap(signame, data)
						detected = True
				else:
					env.log_info(f"--->Ignoring detected signal: {signame_in}.")
					print(f"Press button: {lbl} (retry).")
		return

