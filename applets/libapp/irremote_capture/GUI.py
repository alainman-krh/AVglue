#irremote_capture/GUI.py
#-------------------------------------------------------------------------------
from AVglue.Windows.Actions import *
from AVglue.Actions import *
from IRglue.Base import ControllerCom, ControllerDef
from SerialGlue.Base import PortManager
from TKglue.Builders import TKButtonRows, SEP_ROW
import tkinter as tk


from .Env import env #Use simple environment for capturing IR signals
ctrldef = ControllerDef()
ctrlcom = ControllerCom()


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


#==Helper functions
#===============================================================================
def AddCaptureButton(rows:TKButtonRows, lblmap:dict, fnEHandler, env:OperatingEnvironment):
	rows.row_append(fill="both", expand=True)
	rows.btnpack_change(side="left", fill="both", expand=True)
	rows.createblock(lblmap, fnEHandler, data=env)
	rows.btnpack_change() #Restore Default


#==Button event hanlders
#===============================================================================
def EHremotebtn_click(btn:tk.Button, env:OperatingEnvironment):
	#A real button on the remote
	signame = btn.btnid
	env.signal_trigger(Signal(signame))

def EHcapturebtn_click(btn:tk.Button, env:OperatingEnvironment):
	lblmap = None; siglist_ordered = None
	if "capture_nav" == btn.btnid:
		map = navbtn_lblmap; runorder = navbtn_lyt
	else:
		env.log_info(f"TODO: {btn.btnid}")
		return

	env.log_info("Capturing IR signals...")
	siglbl_ordmap = {signame: lblmap[signame] for signame in siglist_ordered}
	ctrldef.btnlist_capture(siglbl_ordmap, ctrlcom)


def EHspacerbtn_click(btn:tk.Button, env:OperatingEnvironment):
	env.log_info("Spacer button. Clicking does nothing.")


#==Build up GUI
#===============================================================================
appwnd = tk.Tk()  # create parent window
appwnd.title("IRremote-capture")
rowsi = TKButtonRows(appwnd)

#Add channel buttons
#-------------------------------------------------------------------------------
channelbtn_lyt = (
	"1", "2", "3", SEP_ROW,
	"4", "5", "6", SEP_ROW,
	"7", "8", "9", SEP_ROW,
	"ch_clear", "0", "ch_enter", SEP_ROW,
	"ch_guide", "ch-", "ch+", SEP_ROW,
)
rowsi.row_append(6)
rowsi.createblock(channelbtn_lblmap, EHremotebtn_click, data=env, layout=channelbtn_lyt)
AddCaptureButton(rowsi, {"capture_chan": "Capture channels"}, EHcapturebtn_click, env)

#Add navigation buttons
#-------------------------------------------------------------------------------
navbtn_lyt = [
	"nav_cfg", SEP_ROW,
	"nav_menu", "nav_up", "nav_info", SEP_ROW,
	"nav_left", "nav_enter", "nav_right", SEP_ROW,
	"nav_return", "nav_down", "nav_exit", SEP_ROW,
]
rowsi.row_append(4)
rowsi.createblock(navbtn_lblmap, EHremotebtn_click, data=env, layout=navbtn_lyt)
AddCaptureButton(rowsi, {"capture_nav": "Capture navigation"}, EHcapturebtn_click, env)

#Add "app" buttons
#-------------------------------------------------------------------------------
appbtn_lyt = [
	"func_red", "func_green", "func_yellow", "func_blue", SEP_ROW,
	"app_1", "app_2", "app_3", "app_4", SEP_ROW,
]
rowsi.row_append(2)
rowsi.createblock(appbtn_lblmap, EHremotebtn_click, data=env, layout=appbtn_lyt)
AddCaptureButton(rowsi, {"capture_app": "Capture app buttons"}, EHcapturebtn_click, env)

#Add media buttons
#-------------------------------------------------------------------------------
mediabtn_lyt = ( #Implicitly defines the layout
	"rewind", "play", "ff",	SEP_ROW,
	"stop", "pause", "record", SEP_ROW,
	"trackprev", "tracknext", SEP_ROW,
	"vol-", "vol+", "mute", SEP_ROW,
)
rowsi.row_append(4)
rowsi.createblock(mediabtn_lblmap, EHremotebtn_click, data=env, layout=mediabtn_lyt)
AddCaptureButton(rowsi, {"capture_media": "Capture media"}, EHcapturebtn_click, env)

rowsi.row_append() #Easier to grab bottom
rowsi.createblock({"btn_spacer": ""}, EHspacerbtn_click, data=env)


#==Show/start application
#===============================================================================
appwnd.mainloop()