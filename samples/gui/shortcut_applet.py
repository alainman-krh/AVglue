#samples/gui/shortcut_applet.py
#-------------------------------------------------------------------------------
from AVglue.Windows.Actions import *
from AVglue.Actions import *
from PySystemDefs import WindowsWithMacros
from TKglue.EventHandling import wgt_sethandler
import tkinter as tk


#==Define shortcut buttons
#===============================================================================
btninfo_map = {
	#NOTE: button id does not have to match text:
	"suspend": ("Suspend", "SuspendPC"),
	"ctrlpnl": ("Control Panel", "OpenControlPanel"),
	"mycomputer": ("My Computer", "OpenMyComputer"),
	"youtube": ("Youtube", "OpenYoutube"),
	"calc": ("Calc", "OpenCalc"),
	#NOTEPAD?
	"mydocs": ("My documents", "OpenFldDocs"),
	"mymusic": ("My music", "OpenFldMusic"),
	"mypics": ("My pictures", "OpenFldPictures"),
	"myvids": ("My videos", "OpenFldVideos"),
}

#==Add buttons and set event handlers
#===============================================================================
def EHrunbutton_click(btn:tk.Button, env:OperatingEnvironment):
	btnid = btn.btnid
	if btnid is None:
		env.log_error("Unexpected click source.")
		return
	(lbl, signame) = btninfo_map[btnid]
	env.signal_trigger(Signal(signame))


#==Build up GUI
#===============================================================================
#Alias to AVGlue.OperatingEnvironment:
env = WindowsWithMacros.env

appwnd = tk.Tk()  # create parent window
appwnd.title("Productivity shortcuts")

#Define `Frame`s used to place buttons in rows
#-------------------------------------------------------------------------------
NROWS = 4
frame_rows = [
	tk.Frame(appwnd) for i in range(NROWS)
]
for f in frame_rows:
	f.pack(fill="y") #Add elements from left-to-right

#Add shortcut buttons
#-------------------------------------------------------------------------------
SEP = "-"
btnid_list = ( #Implicitly defines the layout
	"suspend", "ctrlpnl", "mycomputer",
	SEP,
	"youtube", "calc",
	SEP,
	"mydocs", "mymusic", "mypics", "myvids",
)
row = 0
for btnid in btnid_list:
	if btnid == SEP:
		row += 1
		continue
	(lbl, signame) = btninfo_map[btnid]
	btn = tk.Button(frame_rows[row], text=lbl)
	btn.btnid = btnid
	wgt_sethandler(btn, EHrunbutton_click, env)
	btn.pack(side="left")


#==Show/start application
#===============================================================================
appwnd.mainloop()