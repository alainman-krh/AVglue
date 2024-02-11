#samples/PySystemDefs/MediaPC1.py
#-------------------------------------------------------------------------------
from AVglue.Base import *
from AVglue.Actions import *
from AVglue.Windows.Actions import *
from AVglue.Windows.Media import Env_InitializeAudio

env = OperatingEnvironment()
Env_InitializeAudio(env)


#==Signal traps
#===============================================================================
traps_mode = SignalTraps({
	"MODEVOL": Action_SwitchMode("default"), #Defined below
	"MODENOTEPAD": Action_SwitchMode("notepad"), #Defined below
})

traps_main = SignalTraps({
	"VOLMUTE": Action_VolumeMute("MASTER", 1),
	"VOLUNMUTE": Action_VolumeMute("MASTER", 0),
	"VOLMUTE-TOGGLE": Action_VolumeMute("MASTER"),
	"VOL+": Action_VolumeUpDown("MASTER", 1),
	"VOL-": Action_VolumeUpDown("MASTER", -1),
	"IR": Action_DecodeInt64("MEDIAPC:IRdecode"), #TODO: Get some example
	"NUMBTN": Action_DecodeInt64("MEDIAPC:VolumeDecode"), #Not necessarily generate from IR signal
})
env.mode_add("default", [traps_mode, traps_main])
env.mode_setactive("default")

def SendKeys_NumToNotepad(env:OperatingEnvironment):
	"""Converts last signal's data_64 to a keypress - and sends to notepad"""
	kstr = f"{env.data_int64}"
	#Hacky way to identify which window gets keypresses
	#(assumes new notepad window exists):
	Action_SendKeys("Untitled - Notepad", kstr).run(env)

traps_notepad = SignalTraps({
	#Don't decode volume signals! Route NUMBTN signals to notepad
	"NUMBTN": Action_ExecuteCustomPy(SendKeys_NumToNotepad),
})
env.mode_add("notepad", [traps_mode, traps_notepad])


#==Decode IR signals
#===============================================================================
decoder_ir = Decoder_Int64()
decoder_ir.add(Action_LogString("Detected: Unknown IR message"), 0x00000000, mask=0x00000000) #Logs all remaining signals
env.decoders_add("MEDIAPC:IRdecode", decoder_ir)


#==Decode NUMBTN signals
#===============================================================================
decode_vol = Decoder_Int64()
#Values 1-9,0 set volume from minimum to maximum:
decode_vol.add(Action_VolumeSet("MASTER", -27), 1)
decode_vol.add(Action_VolumeSet("MASTER", -24), 2)
decode_vol.add(Action_VolumeSet("MASTER", -21), 3)
decode_vol.add(Action_VolumeSet("MASTER", -18), 4)
decode_vol.add(Action_VolumeSet("MASTER", -15), 5)
decode_vol.add(Action_VolumeSet("MASTER", -12), 6)
decode_vol.add(Action_VolumeSet("MASTER", -9), 7)
decode_vol.add(Action_VolumeSet("MASTER", -6), 8)
decode_vol.add(Action_VolumeSet("MASTER", -3), 9)
decode_vol.add(Action_VolumeSet("MASTER",  0), 0)
decode_vol.add(Action_VolumeUpDown("MASTER", 1), 101) #Assumes sending `NUMBTN 101` means volume up
decode_vol.add(Action_VolumeUpDown("MASTER", -1), 100) #Assumes sending `NUMBTN 101` means volume down
decode_vol.add(Action_LogString("Detected: Unknown NUMBTN"), 0x00000000, mask=0x00000000) #Logs all remaining signals
env.decoders_add("MEDIAPC:VolumeDecode", decode_vol)

#Example on adding
#env.actions_add("MEDIAPC:FancySequence", act_something)
