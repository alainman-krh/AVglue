#irremote_capture/GUI.py
#-------------------------------------------------------------------------------
from AVglue.Windows.Actions import *
from AVglue.Actions import *
from TKglue.Builders import TKButtonRows, SEP_ROW
import tkinter as tk


from .Env import env #Use simple environment for capturing IR signals
remote_map = {} #Capture signals in a dict


#==Define shortcut buttons
#===============================================================================
channelbtn_lblmap = { #Channel buttons
	#button-id: label (In case someone wants something different on labels)
	**{f"{num}": f"     {num}     " for num in range(10)},
	"ch_enter": "enter", "ch_clear": "clear",
	"ch-": "ch -", "ch+": "ch +",
	"ch_guide": "guide",
}

navbtn_lblmap = { #Navigation buttons
	"nav_menu": "menu", "nav_info": "info", "nav_cfg": "config",
	"nav_up": "up", "nav_down": "down",
	"nav_enter": "enter",
	"nav_left": "left", "nav_right": "right",
	"nav_return": "return", "nav_exit": "exit",
}

appbtn_lblmap = {
	"func_red": "red", "func_green": "green", "func_yellow": "yellow", "func_blue": "blue",
	"app_1": "app 1", "app_2": "app 2", "app_3": "app 3", "app_4": "app 4"
}

mediabtn_lblmap = { #Media buttons
	#button-id: label (In case someone wants something different on labels)
	"play": "play", "pause": "pause",
	"rewind": "rewind", "ff": "fast fwd",
	"trackprev": "prev", "tracknext": "next",
	"record": "record", "stop": "stop",
	"vol-": "vol -", "vol+": "vol +",
	"mute": "mute", #Most remotes don't have separate mute/unmute buttons
}


#==Button event hanlders
#===============================================================================
def EHmediabtn_click(btn:tk.Button, env:OperatingEnvironment):
	signame = btn.btnid
	env.signal_trigger(Signal(signame))

def EHchannelbtn_click(btn:tk.Button, env:OperatingEnvironment):
	signame = btn.btnid
	env.signal_trigger(Signal(signame))

#==Build up GUI
#===============================================================================
appwnd = tk.Tk()  # create parent window
appwnd.title("IRremote-capture")
rowsi = TKButtonRows(appwnd)

#Add shortcut buttons
#-------------------------------------------------------------------------------
channelbtn_lyt = (
	"1", "2", "3", SEP_ROW,
	"4", "5", "6", SEP_ROW,
	"7", "8", "9", SEP_ROW,
	"ch_clear", "0", "ch_enter", SEP_ROW,
	"ch-", "ch+", SEP_ROW,
	"ch_guide", SEP_ROW,
)
rowsi.row_append(6)
rowsi.createblock(channelbtn_lblmap, EHchannelbtn_click, data=env, layout=channelbtn_lyt)

navbtn_lyt = [
	"nav_cfg", SEP_ROW,
	"nav_menu", "nav_up", "nav_info", SEP_ROW,
	"nav_left", "nav_enter", "nav_right", SEP_ROW,
	"nav_return", "nav_down", "nav_exit", SEP_ROW,
]
rowsi.row_append(4)
rowsi.createblock(navbtn_lblmap, EHchannelbtn_click, data=env, layout=navbtn_lyt)

appbtn_lyt = [
	"func_red", "func_green", "func_yellow", "func_blue", SEP_ROW,
	"app_1", "app_2", "app_3", "app_4", SEP_ROW,
]
rowsi.row_append(2)
rowsi.createblock(appbtn_lblmap, EHchannelbtn_click, data=env, layout=appbtn_lyt)

mediabtn_lyt = ( #Implicitly defines the layout
	"rewind", "play", "ff",	SEP_ROW,
	"stop", "pause", "record", SEP_ROW,
	"trackprev", "tracknext", SEP_ROW,
	"vol-", "vol+", "mute", SEP_ROW,
)
rowsi.row_append(4)
rowsi.createblock(mediabtn_lblmap, EHmediabtn_click, data=env, layout=mediabtn_lyt)

#==Show/start application
#===============================================================================
appwnd.mainloop()