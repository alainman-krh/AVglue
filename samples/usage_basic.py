from AVglue.Base import *
from AVglue.Actions import *
from AVglue.Windows.Actions import *
from AVglue.Windows.Media import Env_InitializeAudio


#==Signals and traps
#===============================================================================
env = OperatingEnvironment()
Env_InitializeAudio(env)

traps_main = SignalTraps({
	"mute": Action_LogString("mute trapped!"),
    "IR": Action_DecodeInt64("NetStreamz:IRdecode") #Decoding is optional
})
env.mode_add("LivingroomMain", [traps_main])
env.mode_setactive("LivingroomMain")

decoder_ir = Decoder_Int64()
decoder_ir.add(Action_LogString("NetStreamz:controller1:play"), 0xABCD123)
decoder_ir.add(Action_LogString("NetStreamz:controller1"), 0xABCD000, mask=0xFFFF000) #Identifies controller... but not button
decoder_ir.add(Action_LogString("NetStreamz:controller2"), 0xABCE000, mask=0xFFFF000)
env.decoders_add("NetStreamz:IRdecode", decoder_ir)
decoder_ir.display()

#==Basic test
#===============================================================================
act_calcopen = Action_ExecuteShell("calc.exe")
#act_calcopen.run(env)


#==More complex test
#===============================================================================
#Will be stored in "PCTAXES" subdirectory (traps/actions tax-related activities)
act_calctest = Action_ExecuteSequence("PCTAXES:CALCTEST", [
	Action_ExecuteShell("calc.exe"),
	Action_Wait(0.5),
	#Action_SendKeys(0, "3{+}14{ENTER}"),
	Action_SendKeys("Calculator", "3{+}14{ENTER}"),
])
success = act_calctest.run(env)

act_mediatest = Action_ExecuteSequence("PCTUBE:MEDIATEST", [
	Action_TriggerLocal(Signal("mute")),
	Action_TriggerLocal(Signal("muteX")),
	Action_TriggerLocal(Signal("mute")),
    Action_TriggerLocal(Signal("IR")),
	Action_TriggerLocal(Signal("IR"), data_int64=0xABCD123), #Not obvious what data is - will get decoded
	Action_TriggerLocal(Signal("IR"), data_int64=0xABCD124), #Not obvious what data is - will get decoded
	Action_TriggerLocal(Signal("IR"), data_int64=0xABCE123), #Not obvious what data is - will get decoded
	Action_Wait(0.5),
	Action_VolumeSet("MASTER", -20),
	Action_Wait(0.5),
	Action_VolumeSet("MASTER", 0),
	Action_VolumeUp("MASTER"),
    Action_VolumeDn("MASTER"),
    Action_LogString("COMPLETE!"),
])
success = act_mediatest.run(env)
