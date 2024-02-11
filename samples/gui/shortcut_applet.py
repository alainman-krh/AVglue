from AVglue.Windows.Actions import *
from AVglue.Actions import *
from PySystemDefs import WindowsWithMacros
import tkinter as tk


#==Build up GUI
#===============================================================================
#Alias to AVGlue.OperatingEnvironment:
env = WindowsWithMacros.env

appwnd = tk.Tk()  # create parent window
appwnd.title("Productivity shortcuts")
btn = {}

#Define `Frame`s used to place buttons in rows
#-------------------------------------------------------------------------------
NROWS = 4
frame_rows = [
	tk.Frame(appwnd) for i in range(NROWS)
]
for f in frame_rows:
	f.pack(fill="y") #Add elements from left-to-right


#==Add buttons and set event handlers
#===============================================================================
def btn_sethandler(btn:tk.Button, action:AbstractAction, env):
	#NOTE: lambda uses variables with local scope here - so we know that
	#whatever arguments are passed to this function will exist only for this
	#one event handler/lambda function.
	btn.configure(command=lambda : action.run(env))

def btn_sethandler_sig(btn:tk.Button, signame, env, data_int64=None):
	#Handler is specifically to trigger a signal (and update scurbber)
	action = Action_TriggerLocal(Signal(signame), data_int64=data_int64)
	btn.configure(command=lambda : action.run(env))

def frame_addbutton(frame, lbl, signame, env):
	btn = tk.Button(frame, text=lbl)
	btn.pack(side="left", fill="y")
	btn_sethandler_sig(btn, signame, env)
	return btn

#==Add buttons with shortcuts
#===============================================================================
btn_d = {
	"Suspend": "SuspendPC",
	"Control Panel": "OpenControlPanel",
	"My Computer": "OpenMyComputer",
}
fref = frame_rows[0]
for (lbl, signame) in btn_d.items():
	btn[lbl] = frame_addbutton(fref, lbl, signame, env)

btn_d = {
	"My documents": "OpenFldDocs",
	"My music": "OpenFldMusic",
	"My pictures": "OpenFldPictures",
	"My videos": "OpenFldVideos",
}
fref = frame_rows[1]
for (lbl, signame) in btn_d.items():
	btn[lbl] = frame_addbutton(fref, lbl, signame, env)


#==Show/start application
#===============================================================================
appwnd.mainloop()