#AVglue/Windows/Media.py: Windows multimedia integrations
#-------------------------------------------------------------------------------
from AVglue.Base import OperatingEnvironment
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL


#==Concrete Actions
#===============================================================================
def Env_InitializeAudio(env:OperatingEnvironment):
	devices = AudioUtilities.GetSpeakers()
	interface = devices.Activate(
		IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
	volume = cast(interface, POINTER(IAudioEndpointVolume))
	#Keep object refrences around
	env.state["WINAUDIO:VOLUME"] = volume
