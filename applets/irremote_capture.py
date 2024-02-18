#applets/irremote_capture.py
#-------------------------------------------------------------------------------
from libapp.irremote_capture.Env import env
from SerialGlue.Base import PortManager


#==
#===============================================================================
env.log_info("COM ports detected on system (Candidates for IR reciever devices):")
portmgr = PortManager()
portmgr.portlist_diplay()

from libapp.irremote_capture.GUI import TKapp as IRapp
app = IRapp()
app.run()

#Test serial:
#from AVglue.SerialSignals import ConnectionManager, OperatingEnvironment
#env = OperatingEnvironment() #Empty
#mgr = ConnectionManager(env)
#mgr.start(connect="COM7")
