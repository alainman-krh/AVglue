from AVglue.Windows.Actions import *
from AVglue.Actions import *
from config_py import MediaPC1
import tkinter as tk


#==Build up GUI
#===============================================================================
appwnd = tk.Tk()  # create parent window
btn = {}

NROWS = 4
frame_rows = [
	tk.Frame(appwnd) for i in range(NROWS)
]
for f in frame_rows:
	f.pack(fill="y") #Add elements from left-to-right

#volume = tk.Label(frame_row1, text="VOLUME")
#vol_up = tk.Button(frame_row1, text="VOL+")
#vol_down = tk.Button(frame_row1, text="VOL-")

fref = frame_rows[0]
for i in (*range(1, 10), 0): #Want 0 last
	btn[i] = tk.Button(fref, text=f"     {i}     ")
	btn[i].pack(side="left", fill="y")
	if 5==i:
		fref = frame_rows[1]

fref = frame_rows[2]
for id in ("VOL-", "VOL+"):
	btn[id] = tk.Button(fref, text=id)
	btn[id].pack(side="left", fill="y")

fref = frame_rows[3]
for id in ("mute", "un-mute", "toggle mute"):
	btn[id] = tk.Button(fref, text=id)
	btn[id].pack(side="left", fill="y")


#==Connect click event handlers
#===============================================================================
#Convenience 
def _handler_setaction(btn:tk.Button, action:AbstractAction, env):
	#NOTE: lambda uses variables with local scope here - so we know that
	#whatever arguments are passed to this function will exist only for this
	#one event handler.
	btn.configure(command=lambda : action.run(env))

def _handler_setsignal(btn:tk.Button, signame, env, data_int64=None):
	action = Action_TriggerLocal(Signal(signame), data_int64=data_int64)
	btn.configure(command=lambda : action.run(env))

#Alias to OperatingEnvironment:
env = MediaPC1.env

#Trigger actions by sending signals (Op-Env decides how to trap/react to signals):
for i in range(10): #0-9
	btn_i:tk.Button = btn[i]
	_handler_setsignal(btn_i, "VOLBTN", env, data_int64=i)

#Maybe the signal traps prefer to jump up/down by 1, 2, 3 steps... who knows?:
_handler_setsignal(btn["VOL-"], "VOL-", env)
_handler_setsignal(btn["VOL+"], "VOL+", env)

#Directly perform actions (don't trigger a signal that needs to be trapped):
#NOTE: By sending signals, environment could be configured with traps that reduce volume (instead of actually muting).
_handler_setaction(btn["mute"], Action_VolumeMute("MASTER", 1), env)
_handler_setaction(btn["un-mute"], Action_VolumeMute("MASTER", 0), env)
_handler_setaction(btn["toggle mute"], Action_VolumeMute("MASTER"), env)


#==Show/start application
#===============================================================================
appwnd.mainloop()