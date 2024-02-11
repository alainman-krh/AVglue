from AVglue.Base import *
from AVglue.Actions import *
from AVglue.Windows.Actions import *
from AVglue.Windows.Media import Env_InitializeAudio

env = OperatingEnvironment()
Env_InitializeAudio(env)


#==Signal traps
#===============================================================================
r"""About Windows shell folders (`shell:FOLDERNAME`)

Windows explorer conveniently supports special `shell:` shortcuts to access shell folders:
-<https://www.howtogeek.com/257715/how-to-open-hidden-system-folders-with-windos-shell-command/>
-<https://www.tenforums.com/tutorials/3109-shell-commands-list-windows-10-a.html>

NOTE: There was also a resource on `microsoft.com` somewhere... but I can no longer find it.
"""

def SystemState_Suspend():
	import ctypes
	ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)

#By having these actions as SignalTraps - external programs/processes/hardware
#can trigger them by sending signals to this process
traps_main = SignalTraps({
    #System:
	#"SuspendPC": Action_ExecuteShell("rundll32.exe powrprof.dll,SetSuspendState 0,1,0"), #NO: Seems to go into hibernate or something
	"SuspendPC": Action_ExecuteCustomPy(SystemState_Suspend),
	"OpenControlPanel": Action_ExecuteShell("explorer shell:ControlPanelFolder"),
	"OpenFldFonts": Action_ExecuteShell("explorer shell:Fonts"),
	"OpenMyComputer": Action_ExecuteShell("explorer shell:MyComputerFolder"),
    #Libraries:
	"OpenLibDocs": Action_ExecuteShell("explorer shell:documentsLibrary"),
    #User folders:
	"OpenFldAppData": Action_ExecuteShell("explorer shell:AppData"),
	"OpenFldAppData_Local": Action_ExecuteShell("explorer shell:Local AppData"),
	"OpenFldDocs": Action_ExecuteShell("explorer shell:Personal"),
	"OpenFldMusic": Action_ExecuteShell("explorer shell:My Music"),
	"OpenFldPictures": Action_ExecuteShell("explorer shell:My Pictures"),
	"OpenFldVideos": Action_ExecuteShell("explorer shell:My Video"),
	"OpenFldFavorites": Action_ExecuteShell("explorer shell:Favorites"),
	"OpenFldDesktop": Action_ExecuteShell("explorer shell:desktop"),
	"OpenFldStartup": Action_ExecuteShell("explorer shell:Startup"),
     
})
env.mode_add("default", [traps_main])
env.mode_setactive("default")

#Action_TriggerLocal(Signal("OpenFldDocs")).run(env)