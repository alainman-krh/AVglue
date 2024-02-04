# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import win32com.client as COM
shell = COM.Dispatch("WScript.Shell")
shell.Run(r"cmd /K CD C:\ & Dir")
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import win32com.client as COM
from time import sleep
shell = COM.Dispatch("WScript.Shell")
x=shell.Run("calc.exe")
shell.AppActivate(x) #More robust than by name
#shell.AppActivate("Calculator")
#shell.AppActivate("Untitled - Notepad")
sleep(1)
shell.SendKeys("3,14{ENTER}")
#Problem: Can't seem to find a way to send numpad(".").. so "." is ignored if "," is expected.
def _sendkeys(shell, msg, twait=0.1):
	if twait is None:
		shell.SendKeys(msg)
		return
	for k in msg:
		print(k)
		shell.SendKeys(k)
		sleep(twait)
#_sendkeys(shell, "3")
#_sendkeys(shell, "{+}", twait=None)
#sleep(0.1)
#_sendkeys(shell, "14")
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Needs calc.exe to be open
import win32ui
import ctypes
from time import sleep
from os import system
#system("calc.exe")
#system("notepad.exe")
sleep(1)
try:
	#wnd = win32ui.FindWindow(None, "Untitled - Notepad")
	wnd = win32ui.FindWindow(None, "Calculator")
except win32ui.error:
	print("win32ui.error")
	pass
except:
	raise Exception("NO")
#wnd.SetForegroundWindow()
sleep(0.2)
#wnd.SetFocus()
sleep(0.2)
seq = "3.14"
print(seq)
#Doesn't seem to work:
result = ctypes.windll.user32.SendInput(seq)
seq = [c for c in seq]
print(seq)
#result = ctypes.windll.user32.SendInput(*seq)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print(volume.GetMute())
print(volume.GetVolumeRange())
print(volume.GetMasterVolumeLevel()) #dB
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
volume.SetMasterVolumeLevel(-20.0, None)
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
