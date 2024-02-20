#samples/PySystemDefs/WindowsMediaControl.py
#-------------------------------------------------------------------------------
from AVglue.Base import *
from AVglue.Actions import *
from AVglue.Windows.Actions import *
from AVglue.Windows.Media import Env_InitializeAudio

env = OperatingEnvironment()
Env_InitializeAudio(env)
env.com_portid = "COM7" #Provides connection info to serial_open()
#NOTE: serial port device should really be accessed by serial name - not "portid".



#==Useful consts
#===============================================================================
IRBTN_POWER = 0x20DF10EF
VK_MEDIA_STOP = 0xB2 #Missing from winCONST


#==Decode IR signals
#===============================================================================
#These codes support repeat:
decoder_ir = Decoder_Int64()
#decoder_ir.add(0x20DF40BF, Action_VolumeUpDown("MASTER", +1)) #VOL+
#decoder_ir.add(0x20DFC03F, Action_VolumeUpDown("MASTER", -1)) #VOL-
#1dB increment:
decoder_ir.add(0x20DF40BF, Action_VolumeUpDown_dB("MASTER", +1)) #VOL+
decoder_ir.add(0x20DFC03F, Action_VolumeUpDown_dB("MASTER", -1)) #VOL-
env.decoders_add("LGremote1:IRdecodeRPT", decoder_ir)

#These codes should ignore repeats:
decoder_ir = Decoder_Int64()
decoder_ir.add(0x20DF906F, Action_SendVirtKey(winCONST.VK_VOLUME_MUTE))
decoder_ir.add(0x20DF0DF2, Action_SendVirtKey(winCONST.VK_MEDIA_PLAY_PAUSE))
decoder_ir.add(0x20DF8D72, Action_SendVirtKey(VK_MEDIA_STOP))
decoder_ir.add(0x20DF718E, Action_SendVirtKey(winCONST.VK_MEDIA_NEXT_TRACK))
decoder_ir.add(0x20DFF10E, Action_SendVirtKey(winCONST.VK_MEDIA_PREV_TRACK))

#For all remaining signals - Check if they are "repeat"-capable:
decoder_ir.add(0x00000000, Action_DecodeInt64("LGremote1:IRdecodeRPT", stashdata=True), mask=0x00000000)
env.decoders_add("LGremote1:IRdecode", decoder_ir)
#decoder_ir.display() #DEBUG


#==Signal traps
#===============================================================================
traps_media = SignalTraps({
	#Direct traps for media control:
	"VOLMUTE": Action_VolumeMute("MASTER", 1),
	"VOLUNMUTE": Action_VolumeMute("MASTER", 0),
	"VOLMUTE-TOGGLE": Action_VolumeMute("MASTER"),
	"VOL+": Action_VolumeUpDown("MASTER", 1),
	"VOL-": Action_VolumeUpDown("MASTER", -1),
	
    #Traps specifically for signals from IR remote:
	"IR": Action_DecodeInt64("LGremote1:IRdecode", clear_stash="LGremote1:IRdecodeRPT"), #Signals that shouldn't repeat
	"IR-RPT": Action_DecodeInt64_Repeat("LGremote1:IRdecodeRPT"), #Uses NEC protocol... repeat signal
})
env.mode_add("default", [traps_media])
env.mode_setactive("default")

#Last line