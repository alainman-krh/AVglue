from AVglue.Windows.Actions import *
from AVglue.Actions import *
from config_py import MediaPC1
import tkinter as tk


#==Build up GUI
#===============================================================================
appwnd = tk.Tk()  # create parent window
btn = {}

frame_rows = [
	tk.Frame(appwnd),
	tk.Frame(appwnd),
	tk.Frame(appwnd),
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
for id in ("mute", "un-mute", "toggle mute"):
	btn[id] = tk.Button(fref, text=id)
	btn[id].pack(side="left", fill="y")


#==Connect click event handlers
#===============================================================================
#Shorhand to trigger actions:
def _send_signal(signame, data=None):
	act = Action_TriggerLocal(Signal(signame), data_int64=data)
	act.run(MediaPC1.env)
#Action_TriggerLocal(Signal("VOLMUTE")),

for i in range(10): #0-9
	btn_i:tk.Button = btn[i]
	#IMPORTANT: Lambda needs to get default _i=i... otherwise all buttons access same "i":
	btn_i.configure(command=lambda _i=i : _send_signal("VOLBTN", _i))


#==Show/start application
#===============================================================================
appwnd.mainloop()