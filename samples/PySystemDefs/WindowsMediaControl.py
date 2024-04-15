#samples/PySystemDefs/WindowsMediaControl.py
#-------------------------------------------------------------------------------
from AVglue.Base import *
from AVglue.Actions import *
from AVglue.Windows.Actions import *
from AVglue.Windows.Media import Env_InitializeAudio

env = OperatingEnvironment()
Env_InitializeAudio(env)
env.com_portid = "COM9" #Provides connection info to serial_open()
#NOTE: serial port device should really be accessed by serial name - not "portid".



#==Useful consts
#===============================================================================
IRBTN_POWER = 0x20DF10EF
VK_MEDIA_STOP = 0xB2 #Missing from winCONST
VK_ALT = winCONST.VK_LMENU


#==Decode IR signals
#===============================================================================
#These codes support repeat:
decoder_ir = Decoder_Int64()
#1 "percent" increment (more like TV volume control):
#decoder_ir.add(0x20DF40BF, Action_VolumeUpDown("MASTER", +1)) #VOL+
#decoder_ir.add(0x20DFC03F, Action_VolumeUpDown("MASTER", -1)) #VOL-
#1dB increment (more like typical audio equipment):
decoder_ir.add(0x20DF40BF, Action_VolumeUpDown_dB("MASTER", +1)) #VOL+
decoder_ir.add(0x20DFC03F, Action_VolumeUpDown_dB("MASTER", -1)) #VOL-

#Navigation buttons:
#decoder_ir.add(0x20DF02FD, Action_SendVirtKey(winCONST.VK_LEFT, modctrl=True))
decoder_ir.add(0x20DF02FD, Action_SendVirtKey(winCONST.VK_UP))
decoder_ir.add(0x20DF827D, Action_SendVirtKey(winCONST.VK_DOWN))
decoder_ir.add(0x20DFE01F, Action_SendVirtKey(winCONST.VK_LEFT))
decoder_ir.add(0x20DF609F, Action_SendVirtKey(winCONST.VK_RIGHT))

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
	"IRNEC": Action_DecodeInt64("LGremote1:IRdecode", clear_stash="LGremote1:IRdecodeRPT"), #Signals that shouldn't repeat
	"IRNEC-RPT": Action_DecodeInt64_Repeat("LGremote1:IRdecodeRPT"), #Uses NEC protocol... repeat signal
})
env.mode_add("default", [traps_media])
env.mode_setactive("default")

#Last line