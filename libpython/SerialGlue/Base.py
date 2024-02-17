#SerialGlue/Base.py
#-------------------------------------------------------------------------------
import os
from copy import copy

if os.name == 'nt':  # sys.platform == 'win32':
	from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
	from serial.tools.list_ports_posix import comports
else:
	raise ImportError("OS not supported: {os.name}.")


#==PortManager
#===============================================================================
class PortManager:
	def __init__(self) -> None:
		self.port_list = [] #List of port_info=(port, desc, hwid)
	
	def portlist_refresh(self):
		#Copy port_info - just in case iterator doesn't return copies itself
		iterator = sorted(comports())
		self.port_list = tuple(copy(port_info) for port_info in iterator)

	def portlist_diplay(self, refresh=True):
		if refresh:
			self.portlist_refresh()
		for (port, desc, hwid) in self.port_list:
			print(f"{port:20}")
			print(f"    desc: {desc}")
			print(f"    hwid: {hwid}")

	def portid_fromserialno(self, sn):
		sn = sn.lower()
		for (port, desc, hwid) in self.port_list:
			hwid_split = hwid.split()
			for v in hwid_split:
				if "SER=" in v:
					sn_i = v.split("=")[-1]
					if sn_i.lower() == sn:
						return port
		return None


#==Quick test
#===============================================================================
def _testcode():
	sn = "SOMESERIALNO"
	mgr = PortManager()
	mgr.portlist_diplay()
	portid = mgr.portid_fromserialno(sn)
	print(portid)

if __name__ == '__main__':
    _testcode()
#Last line