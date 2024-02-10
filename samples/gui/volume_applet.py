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
#Shorhand to trigger actions:
def _send_signal(env, signame, data=None):
	act = Action_TriggerLocal(Signal(signame), data_int64=data)
	act.run(env)
#Action_TriggerLocal(Signal("VOLMUTE")),

env = MediaPC1.env #Alias
for i in range(10): #0-9
	btn_i:tk.Button = btn[i]
	#IMPORTANT: Lambda needs to get default _i=i... otherwise all buttons access same "i":
	btn_i.configure(command=lambda _env=env, _i=i : _send_signal(_env, "VOLBTN", _i))

btn["VOL-"].configure(command=lambda _env=env: _send_signal(_env, "VOL-"))
btn["VOL+"].configure(command=lambda _env=env: _send_signal(_env, "VOL+"))
btn["mute"].configure(command=lambda _env=env: _send_signal(_env, "VOLMUTE"))
btn["un-mute"].configure(command=lambda _env=env: _send_signal(_env, "VOLUNMUTE"))
btn["toggle mute"].configure(command=lambda _env=env: _send_signal(_env, "VOLMUTE-TOGGLE"))


#==Show/start application
#===============================================================================
appwnd.mainloop()