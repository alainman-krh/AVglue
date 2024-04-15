#AVglue/IRController.py
#-------------------------------------------------------------------------------
from .Base import Signal, OperatingEnvironment
from SerialGlue.LossyMessaging import LossySerial #Not necessary - but suggested
from serial import Serial
from time import time as time_now
import toml


def _IRdata_tostr(data):
	return f"0x{data:02X}" #Display at least 2 nibbles


#==ControllerDef
#===============================================================================
class ControllerDef:
	"""Controller definition"""

	def __init__(self):
		self.map = {}
		self.devid = None #Device ID. Typically serial number of serial device
		self.siglast_data = 0
		self.siglast_timestamp = time_now()
		self.siglast_timeout = 2
		self.verbose = False
		pass

#-------------------------------------------------------------------------------
	def map_asstring(self):
		return {signame: _IRdata_tostr(data) for (signame, (irsig, data)) in self.map.items()}

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
	def btn_updatemap(self, signame, irsig:Signal, data):
		self.siglast_timestamp = time_now()
		self.map[signame] = (irsig, data)
		self.siglast_data = (irsig, data)

#-------------------------------------------------------------------------------
	def btnlist_capture(self, siglbl_ordmap:dict, env:OperatingEnvironment, ircom:LossySerial):
		for (signame, lbl) in siglbl_ordmap.items():
			print(f"Press button: {lbl}.")
			detected = False
			while not detected:
				msg = ircom.readline()
				if msg is None: #Probably timeout
					continue
				msg = msg.decode("utf-8")
				#print(msg) #DEBUG
				(irsig, data) = env.message_tosignal(msg)
				if irsig is None:
					env.log_error("--->Error trying to capture IR signal:")
					env.log_error(f"--->{msg}")
					continue

				signame_ir = irsig.id
				if "RPT" in signame_ir:
					continue #Those don't count
				elif "IR" == signame_ir[:2]:
					self.btn_updatemap(signame, irsig, data)
					detected = True
				else:
					env.log_info(f"--->Ignoring detected signal: {signame_ir}.")
					print(f"Press button: {lbl} (retry).")
		return

