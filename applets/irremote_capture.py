#applets/irremote_capture.py
#-------------------------------------------------------------------------------
from libapp.irremote_capture.Env import env
from SerialGlue.Base import PortManager
from serial import Serial


#==
#===============================================================================
env.log_info("COM ports detected on system (Candidates for IR reciever devices):")
portmgr = PortManager()
portmgr.portlist_diplay()

from libapp.irremote_capture.GUI import TKapp as IRapp
com = Serial("COM7")
app = IRapp(env, com)
app.run()

#Test serial:
#from AVglue.SerialSignals import ConnectionManager, OperatingEnvironment
#env = OperatingEnvironment() #Empty
#mgr = ConnectionManager(env)
#mgr.start(connect="COM7")
