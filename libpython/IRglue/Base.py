#IRglue/Base.py
#-------------------------------------------------------------------------------
import toml
from serial import Serial


#==ControllerCom
#===============================================================================
class ControllerCom:
	def __init__(self, io=None) -> None:
		self.io = io
		pass

	def log_error(self, msg):
		print(msg)

	def connect(self, port):
		if self.io != None:
			raise Exception("Already connected!")
		self.io = Serial(port)

	def message_tosignal(self, msg:str):
		RESULT_NOSIG = (None, 0)
		tokens = msg.split()
		N = len(tokens)
		if N < 1:
			return RESULT_NOSIG
		elif N > 2:
			self.log_error(f"Only supports signals with up to 1 optional argument:\n`{msg}`")
			return RESULT_NOSIG

		data = None
		if N > 1: #We have data
			dstr = tokens[1]
			if "0x" == dstr[:2]:
				data = int(dstr, 16)
			else:
				data = int(dstr)

		signame = tokens[0]
		return (signame, data)


#==ControllerDef
#===============================================================================
class ControllerDef:
	"""Controller definition"""
	def __init__(self):
		self.map = {}
		self.devid = None #Device ID. Typically sereial number of serial device
		pass

	def btnlist_capture(siglbl_ordmap, com:ControllerCom):
		for (sig, lbl) in siglbl_ordmap:
			print(f"Press button: {lbl}.")
			com.ser
		return

	def write(self, filepath):
		toml.dump(self.map, filepath)

