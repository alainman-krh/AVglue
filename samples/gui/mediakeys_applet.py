#samples/gui/volume_applet.py
#-------------------------------------------------------------------------------
from AVglue.Windows.Actions import *
from AVglue.Actions import *
from TKglue.EventHandling import wgt_sethandler
import tkinter as tk
from os.path import basename

APPNAME = basename(__file__)

#Alias to AVGlue.OperatingEnvironment:
from PySystemDefs import MediaPC1
env = MediaPC1.env


#Some useful constants:
#-------------------------------------------------------------------------------
#Some are just listed here; others are added (missing from winCONST)
VK_SLEEP = 0x5F #Missing from winCONST... but doesn't seem to work
winCONST.VK_VOLUME_MUTE #Toggle
winCONST.VK_VOLUME_DOWN
winCONST.VK_VOLUME_UP
winCONST.VK_MEDIA_PLAY_PAUSE
VK_MEDIA_STOP = 0xB2 #Missing from winCONST
winCONST.VK_MEDIA_NEXT_TRACK
winCONST.VK_MEDIA_PREV_TRACK
VK_BROWSER_FAVORITES   = 0xAB #Toggle browser favorites
#Don't think these work:
VK_LAUNCH_MAIL         = 0xB4 #Start Mail key
VK_LAUNCH_MEDIA_SELECT = 0xB5 #Select Media key
VK_LAUNCH_APP1         = 0xB6 #Start Application 1 key
VK_LAUNCH_APP2         = 0xB7 #Start Application 2 key

vk = VK_LAUNCH_APP1 
#vk = winCONST.VK_MEDIA_PLAY_PAUSE
#Action_ExecuteShell(r"'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\firefox.exe'").run(env)
#cmd='explorer "https://google.com"'
#Action_ExecuteShell(cmd).run(env); Action_Wait(1).run(env)
Action_SendVirtKey(vk).run(env)
app = "Calculator"
#Action_SendKeys("3", app, twait=0.5).run(env)
#Action_SendVirtKey(winCONST.VK_DECIMAL).run(env)
#Action_SendKeys("14").run(env)

print(f"WARN: {APPNAME} not yet implemented.")