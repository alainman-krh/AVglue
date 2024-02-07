from AVglue.Base import *
from AVglue.Actions import *
from AVglue.Windows.Actions import *
from AVglue.Windows.Media import Env_InitializeAudio


env = OperatingEnvironment()
Env_InitializeAudio(env)


#==Signal traps
#===============================================================================
traps_main = SignalTraps({
	"VOLMUTE": Action_VolumeMute("MASTER"),
    "IR": Action_DecodeInt64("MEDIAPC:IRdecode"), #TODO: Get some example
    "VOLBTN": Action_DecodeInt64("MEDIAPC:VolumeDecode"),
})
env.mode_add("LivingroomMain", [traps_main])
env.mode_setactive("LivingroomMain")


#==Decode IR signals
#===============================================================================
decoder_ir = Decoder_Int64()
decoder_ir.add(Action_LogString("Detected: Unknown IR message"), 0x00000000, mask=0x00000000) #Logs all remaining signals
env.decoders_add("MEDIAPC:IRdecode", decoder_ir)


#==Decode VOLBTN signals
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
decode_vol.add(Action_VolumeUpDown("MASTER", 1), 101) #Assumes sending `VOLBTN 101` means volume up
decode_vol.add(Action_VolumeUpDown("MASTER", -1), 100) #Assumes sending `VOLBTN 101` means volume down
decode_vol.add(Action_LogString("Detected: Unknown VOLBTN"), 0x00000000, mask=0x00000000) #Logs all remaining signals
env.decoders_add("MEDIAPC:VolumeDecode", decode_vol)

#Example on adding
#env.actions_add("MEDIAPC:FancySequence", act_something)
