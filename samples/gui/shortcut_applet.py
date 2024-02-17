#samples/gui/shortcut_applet.py
#-------------------------------------------------------------------------------
from AVglue.Windows.Actions import *
from AVglue.Actions import *
from PySystemDefs import WindowsWithMacros
from TKglue.Builders import TKButtonRows, SEP_ROW
import tkinter as tk


#==Define shortcut buttons
#===============================================================================
btnshortcuts_lblmap = { #Shortcut buttons
	#button-id: label (In case someone wants something different on labels)
	"SuspendPC": "Suspend",
	"OpenControlPanel": "Control Panel",
	"OpenMyComputer": "My Computer",
	"OpenYoutube": "Youtube",
	"OpenCalc": "Calc",
	#NOTEPAD?
	"OpenFldDocs": "My documents",
	"OpenFldMusic": "My music",
	"OpenFldPictures": "My pictures",
	"OpenFldVideos": "My videos",
}


#==Add buttons and set event handlers
#===============================================================================
def EHrunbutton_click(btn:tk.Button, env:OperatingEnvironment):
	signame = btn.btnid
	if signame is None:
		env.log_error("Unexpected click source.")
		return
	env.signal_trigger(Signal(signame))


#==Build up GUI
#===============================================================================
#Alias to AVGlue.OperatingEnvironment:
env = WindowsWithMacros.env

appwnd = tk.Tk()  # create parent window
appwnd.title("Productivity shortcuts")

#Add shortcut buttons
#-------------------------------------------------------------------------------
btnshortcuts_lyt = ( #Implicitly defines the layout
	"SuspendPC", "OpenControlPanel", "OpenMyComputer",
	SEP_ROW,
	"OpenYoutube", "OpenCalc",
	SEP_ROW,
	"OpenFldDocs", "OpenFldMusic", "OpenFldPictures", "OpenFldVideos",
)
rowsi = TKButtonRows(appwnd)
rowsi.append(4)
rowsi.createblock(btnshortcuts_lblmap, btnshortcuts_lyt, EHrunbutton_click, env)


#==Show/start application
#===============================================================================
appwnd.mainloop()