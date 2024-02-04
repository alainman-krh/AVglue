from AVglue.Base import OperatingEnvironment, SignalTraps
from AVglue.Actions import *
from AVglue.Windows.Actions import Action_SendKeys


#==Signals and traps
#===============================================================================
env = OperatingEnvironment()

traps_main = SignalTraps({
	"mute": Action_LogString("mute trapped!"),
})
env.mode_add("LivingroomMain", [traps_main])
env.mode_setactive("LivingroomMain")


#==Basic test
#===============================================================================
act_calcopen = Action_ExecuteShell("calc.exe")
#act_calcopen.run(env)


#==More complex test
#===============================================================================
#Will be stored in "PCTAXES" subdirectory (traps/actions tax-related activities)
act_calctest = Action_ExecuteSequence("PCTAXES:CALCTEST", [
	Action_TriggerLocalSignal("mute"),
	Action_TriggerLocalSignal("muteX"),
	Action_ExecuteShell("calc.exe"),
	Action_Wait(0.5),
	Action_SendKeys(0, "3{+}14{ENTER}"),
	Action_TriggerLocalSignal("mute"),
])

act_calctest.run(env)