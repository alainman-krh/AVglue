#samples/mediacontrol_applet.py
#-------------------------------------------------------------------------------
from AVglue.Base import OperatingEnvironment, Signal
from PySystemDefs import WindowsMediaControl #Assume current folder is in path
from SerialGlue.Base import PortManager
from SerialGlue.LossyMessaging import LossySerial
from os.path import basename
from serial import Serial

APPNAME = basename(__file__)
env = WindowsMediaControl.env #Alias
env.verbose = False


#==Configuration/helper functions
#===============================================================================
env.log_info("COM ports detected on system (Candidates for IR reciever devices):")
portmgr = PortManager()
portmgr.portlist_diplay()

def serial_open(env:OperatingEnvironment):
	portid = env.com_portid
	portmgr.portlist_refresh()
	ctrlserialno = portmgr.serialno_get(portid)
	com = Serial(portid)
	env.log_info(f"Using SN={ctrlserialno} on {portid}")
	return com


#==Main program
#===============================================================================
print()
env.log_info(f"Initializing {APPNAME}...")
com:Serial = serial_open(env)
ircom = LossySerial(com, timeout=0)

while True:
	msg = ircom.readline()
	if msg is None: #Probably timeout
		ircom.reset_input_buffer()
		continue
	msg = msg.decode("utf-8")
	(sig, data) = env.message_tosignal(msg)
	if sig is None:
		env.log_error("--->Error trying to capture IR signal:")
		env.log_error(f"--->{msg}")
		continue
	elif WindowsMediaControl.IRBTN_POWER == data:
		env.log_info("Quitting")
		break

	signame_in = sig.id
	if signame_in in ("IR", "IR-RPT"):
		env.signal_trigger(Signal(signame_in), data_int64=data)
	else:
		env.log_info(f"--->Ignoring detected signal: {signame_in}.")

#Last line