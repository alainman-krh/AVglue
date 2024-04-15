#applets/irremotecodes_capture.py
#-------------------------------------------------------------------------------
from libapp.irremote_capture.GUI import TKapp as IRapp
from libapp.irremote_capture.Env import env
from SerialGlue.Base import PortManager

	  
#==Launch app
#===============================================================================
env.log_info("COM ports detected on system (Candidates for IR reciever devices):")
portmgr = PortManager()
portmgr.portlist_diplay()

print()
env.log_info(f"Launching IRremote-capture...")
env.verbose=False
app = IRapp(env, "COM9")
app.run()


#==Tests
#===============================================================================
if False: #Test capture:
	from types import SimpleNamespace
	btn = SimpleNamespace(btnid="capture_app")
	app.ctrldef.verbose=True
	app.EHcapturebtn_click(btn, app)

if False: #Test serial:
	from AVglue.SerialSignals import ConnectionManager, OperatingEnvironment
	env = OperatingEnvironment() #Empty
	mgr = ConnectionManager(env)
	mgr.start(connect="COM7")

#Last line