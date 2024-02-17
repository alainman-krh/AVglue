#SerialGlue/Base.py
#-------------------------------------------------------------------------------
import os

if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
else:
    raise ImportError("OS not supported: {os.name}.")


#==comport_find
#===============================================================================
def comport_find(sn:str):
	sn = sn.lower()
	iterator = sorted(comports())

	for n, (port, desc, hwid) in enumerate(iterator, 1):
		hwid_split = hwid.split()
		for v in hwid_split:
			if "SER=" in v:
				sn_i = v.split("=")[-1]
				if sn_i.lower() == sn:
					return port
	return None

sn = "SOMESERIALNO"
port = comport_find(sn)
print(port)
