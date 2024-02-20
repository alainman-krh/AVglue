#applets/irremotecodes_display.py
#-------------------------------------------------------------------------------
from libapp.irremote_capture.Env import env
from AVglue.Base import OperatingEnvironment, Signal
from SerialGlue.Base import PortManager
from SerialGlue.LossyMessaging import LossySerial
from os.path import basename
from serial import Serial

APPNAME = basename(__file__)
env.com_portid = "COM7" #Provides connection info to serial_open()
#NOTE: serial port device should really be accessed by serial name - not "portid".
env.verbose = False
IRBTN_POWER = 0xABCD #TODO


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
	elif False: #IRBTN_POWER == data: #TODO
		env.log_info("Quitting")
		break

	sigid = sig.id
	datastr = "None" if (data is None) else f"0x{data:02X}"
	env.log_info(f"Signal detected: {sigid} ({datastr}).")

#Last line