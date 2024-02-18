#irremote_capture/GUI.py
#-------------------------------------------------------------------------------
from AVglue.Base import Signal, OperatingEnvironment
from IRglue.Base import ControllerCom, ControllerDef
from SerialGlue.Base import PortManager
from TKglue.Builders import TKButtonRows, SEP_ROW
import tkinter as tk


from .Env import env #Use simple environment for capturing IR signals
ctrldef = ControllerDef()
ctrlcom = ControllerCom()


#==Define IRremote buttons
#===============================================================================
channelbtn_lblmap = { #Channel buttons
	#button-id: label (In case someone wants something different on labels)
	**{f"{num}": f"     {num}     " for num in range(10)},
	"ch_enter": "enter", "ch_clear": "clear",
	"ch-": "ch -", "ch+": "ch +",
	"ch_guide": "guide",
}
channelbtn_lyt = (
	"1", "2", "3", SEP_ROW,
	"4", "5", "6", SEP_ROW,
	"7", "8", "9", SEP_ROW,
	"ch_clear", "0", "ch_enter", SEP_ROW,
	"ch_guide", "ch-", "ch+",
)

#-------------------------------------------------------------------------------
navbtn_lblmap = { #Navigation buttons
	"nav_menu": "menu", "nav_info": "info", "nav_cfg": "config",
	"nav_up": "up", "nav_down": "down",
	"nav_enter": "enter",
	"nav_left": "left", "nav_right": "right",
	"nav_return": "return", "nav_exit": "exit",
}
navbtn_lyt = [
	"nav_cfg", SEP_ROW,
	"nav_menu", "nav_up", "nav_info", SEP_ROW,
	"nav_left", "nav_enter", "nav_right", SEP_ROW,
	"nav_return", "nav_down", "nav_exit",
]

#-------------------------------------------------------------------------------
appbtn_lblmap = {
	"func_red": "red", "func_green": "green", "func_yellow": "yellow", "func_blue": "blue",
	"app_1": "app 1", "app_2": "app 2", "app_3": "app 3", "app_4": "app 4"
}
appbtn_lyt = [
	"func_red", "func_green", "func_yellow", "func_blue", SEP_ROW,
	"app_1", "app_2", "app_3", "app_4",
]

#-------------------------------------------------------------------------------
mediabtn_lblmap = { #Media buttons
	#button-id: label (In case someone wants something different on labels)
	"play": "play", "pause": "pause",
	"rewind": "rewind", "ff": "fast fwd",
	"trackprev": "prev", "tracknext": "next",
	"record": "record", "stop": "stop",
	"vol-": "vol -", "vol+": "vol +",
	"mute": "mute", #Most remotes don't have separate mute/unmute buttons
}
mediabtn_lyt = (
	"rewind", "play", "ff",	SEP_ROW,
	"stop", "pause", "record", SEP_ROW,
	"trackprev", "tracknext", SEP_ROW,
	"vol-", "vol+", "mute",
)


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

def EHspacerbtn_click(btn:tk.Button, env:OperatingEnvironment):
	env.log_info("Spacer button. Clicking does nothing.")


#==GUI Application
#===============================================================================
class TKapp:
	def __init__(self, env:OperatingEnvironment, apptitle="IRremote-capture"):
		self.env = env
		self.apptitle = apptitle

#-------------------------------------------------------------------------------
	@staticmethod
	def EHcapturebtn_click(btn:tk.Button, app):
		lblmap = None; siglist_ordered = None
		if "capture_nav" == btn.btnid:
			lblmap = navbtn_lblmap; siglist_ordered = navbtn_lyt
		else:
			app.env.log_info(f"TODO: {btn.btnid}")
			return

		app.env.log_info("Capturing IR signals...")
		siglist_ordered = filter(lambda item: item != SEP_ROW, siglist_ordered)
		siglbl_ordmap = {signame: lblmap[signame] for signame in siglist_ordered}
		ctrldef.btnlist_capture(siglbl_ordmap, ctrlcom)

#-------------------------------------------------------------------------------
	def build_gui(self):
		appwnd = tk.Tk()  # create parent window
		appwnd.title(self.apptitle)
		rows = TKButtonRows(appwnd)

#Add channel buttons
#-------------------------------------------------------------------------------
		rows.createblock(channelbtn_lblmap, EHremotebtn_click, data=env, layout=channelbtn_lyt, row_autoappend=True)
		AddCaptureButton(rows, {"capture_chan": "Capture channels"}, TKapp.EHcapturebtn_click, self)

#Add navigation buttons
#-------------------------------------------------------------------------------
		rows.createblock(navbtn_lblmap, EHremotebtn_click, data=env, layout=navbtn_lyt, row_autoappend=True)
		AddCaptureButton(rows, {"capture_nav": "Capture navigation"}, TKapp.EHcapturebtn_click, self)

#Add "app" buttons
#-------------------------------------------------------------------------------
		rows.createblock(appbtn_lblmap, EHremotebtn_click, data=env, layout=appbtn_lyt, row_autoappend=True)
		AddCaptureButton(rows, {"capture_app": "Capture app buttons"}, TKapp.EHcapturebtn_click, self)

#Add media buttons
#-------------------------------------------------------------------------------
		rows.createblock(mediabtn_lblmap, EHremotebtn_click, data=env, layout=mediabtn_lyt, row_autoappend=True)
		AddCaptureButton(rows, {"capture_media": "Capture media"}, TKapp.EHcapturebtn_click, self)

#Add button spacer (easier to resize window)
#-------------------------------------------------------------------------------
		rows.row_append()
		rows.createblock({"btn_spacer": ""}, EHspacerbtn_click, data=env)

#Keep references
#-------------------------------------------------------------------------------
		self.appwnd = appwnd
		self.btnrows = rows

#-------------------------------------------------------------------------------
	def run(self):
		self.build_gui()
		return self.appwnd.mainloop() #Show/start application