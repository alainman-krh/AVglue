#irremote_capture/GUI.py
#-------------------------------------------------------------------------------
from AVglue.Windows.Actions import *
from AVglue.Actions import *
from TKglue.Builders import TKButtonRows, SEP_ROW
import tkinter as tk


#==Define shortcut buttons
#===============================================================================
mediabtn_lblmap = { #Base media buttons
	#button-id: label (In case someone wants something different on labels)
	"play": "play",
	"pause": "pause",
	"rewind": "rewind",
	"ff": "fast fwd",
	"trackprev": "prev",
	"tracknext": "next",
	"record": "record",
	"stop": "stop",
	"vol+": "vol +",
	"vol-": "vol -",
	"mute": "mute", #Most remotes don't have separate mute/unmute buttons
}

numpad_lblmap = { #Base media buttons
	#button-id: label (In case someone wants something different on labels)
	**{f"ch{num}": f"{num}" for num in range(10)},
	"ch_clear": "clear",
	"ch_enter": "enter",
}


#==Build up GUI
#===============================================================================
from .Env import env #Use simple environment for capturing IR signals

appwnd = tk.Tk()  # create parent window
appwnd.title("IRremote-capture")


#==Button event hanlder
#===============================================================================
def EHmediabtn_click(btn:tk.Button, env:OperatingEnvironment):
	signame = btn.btnid
	if signame is None:
		env.log_error("Unexpected click source.")
		return
	env.signal_trigger(Signal(signame))


#Add shortcut buttons
#-------------------------------------------------------------------------------
mediabtn_lyt = ( #Implicitly defines the layout
	"rewind", "play", "ff",
	SEP_ROW,
	"stop", "pause", "record",
	SEP_ROW,
	"trackprev", "tracknext",
)

rowsi = TKButtonRows(appwnd)
rowsi.row_append(4)
rowsi.createblock(mediabtn_lblmap, EHmediabtn_click, data=env, layout=mediabtn_lyt)


#==Show/start application
#===============================================================================
appwnd.mainloop()