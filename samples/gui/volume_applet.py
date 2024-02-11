from AVglue.Windows.Actions import *
from AVglue.Actions import *
from AVglue.PythonTools import clamp2range
from config_py import MediaPC1
import tkinter as tk


#==Fancy volume scrubber
#===============================================================================
class VolumeScrubber:
	"""Wrapper class to handle complexity of tk.Scrollbar"""
	def __init__(self, parent, env, vol_init=-100):
		self.w = tk.Scrollbar(parent, orient="horizontal")
		self.env = env
		self.wbox = 0.2 #With of scrollbox
		self.w.pack(fill="x")
		self.valrange = (-30.0, 0.0) #dB (float)
		self.val_set(vol_init)
		self._scrubhandler_set()
		self.pagestep = 3.0 #dB (float)

	def _pos_update(self, newpos):
		self.w.set(newpos, newpos+self.wbox)
	
	def _pos_get(self):
		(l, h) = self.w.get()
		posmax = 1-self.wbox
		scale = 1/posmax
		return l*scale

	def val_get(self):
		(l, h) = self.w.get()
		posmax = 1-self.wbox
		rng = self.valrange
		delta = rng[1]-rng[0]
		scale = delta/posmax
		v = rng[0] + l*scale
		return clamp2range(rng, v)

	def val_set(self, newval):
		#Should not trigger pos_update()
		posmax = 1-self.wbox
		rng = self.valrange
		delta = rng[1]-rng[0]
		scale = posmax/delta
		newpos = (newval-rng[0])*scale
		self._pos_update(newpos) #Should not trigger pos_update()

	def refresh(self):
		volume = self.env.state["WINAUDIO:VOLUME"]
		vol = volume.GetMasterVolumeLevel()
		self.val_set(vol)
		#print(vol)

	def pos_update(self, action:str, newpos, unit=None):
		newpos = float(newpos)
		#print(f"{action}, {newpos}, {unit}")
		if "moveto" == action: #Absolute value
			self._pos_update(newpos)
		elif "scroll" == action:
			oldval = self.val_get()
			delta = newpos*self.pagestep #Bump up volume by pagestep
			self.val_set(oldval+delta)
		vol = self.val_get()
		Action_VolumeSet("MASTER", vol).run(self.env)

	def _scrubhandler_set(self):
		self.w.configure(command=lambda p1, p2, p3=None : self.pos_update(p1, p2, p3))


#==Build up GUI
#===============================================================================
#Alias to AVGlue.OperatingEnvironment:
env = MediaPC1.env

appwnd = tk.Tk()  # create parent window
appwnd.title = "Volume control"
btn = {}

#First row: volume scrollbar
#-------------------------------------------------------------------------------
volscrub = VolumeScrubber(appwnd, env)

#Define `Frame`s used to place buttons in rows
#-------------------------------------------------------------------------------
NROWS = 4
frame_rows = [
	tk.Frame(appwnd) for i in range(NROWS)
]
for f in frame_rows:
	f.pack(fill="y") #Add elements from left-to-right

#Add numbered buttons (volume presets)
#-------------------------------------------------------------------------------
fref = frame_rows[0]
for i in (*range(1, 10), 0): #Want 0 last
	btn[i] = tk.Button(fref, text=f"     {i}     ")
	btn[i].pack(side="left", fill="y")
	if 5==i:
		fref = frame_rows[1]

#Add volume -/+ buttons
#-------------------------------------------------------------------------------
fref = frame_rows[2]
for id in ("VOL-", "VOL+"):
	btn[id] = tk.Button(fref, text=id)
	btn[id].pack(side="left", fill="y")

#Add mute buttons
#-------------------------------------------------------------------------------
fref = frame_rows[3]
for id in ("mute", "un-mute", "toggle mute"):
	btn[id] = tk.Button(fref, text=id)
	btn[id].pack(side="left", fill="y")


#==Connect click event handlers
#===============================================================================
def volume_runaction(btn:tk.Button, action:AbstractAction, env):
	action.run(env)
	volscrub.refresh()

#Convenience functions
def volumebtn_sethandler(btn:tk.Button, action:AbstractAction, env):
	#NOTE: lambda uses variables with local scope here - so we know that
	#whatever arguments are passed to this function will exist only for this
	#one event handler/lambda function.
	btn.configure(command=lambda : volume_runaction(btn, action, env))

def volumebtn_sethandler_sig(btn:tk.Button, signame, env, data_int64=None):
	#Handler is specifically to trigger a signal (and update scurbber)
	action = Action_TriggerLocal(Signal(signame), data_int64=data_int64)
	btn.configure(command=lambda : volume_runaction(btn, action, env))

#Trigger actions by sending signals (Op-Env decides how to trap/react to signals):
#-------------------------------------------------------------------------------
for i in range(10): #0-9
	btn_i:tk.Button = btn[i]
	volumebtn_sethandler_sig(btn_i, "VOLBTN", env, data_int64=i)

#Maybe user wants the signal traps prefer to jump up/down by 1, 2, 3 steps... who knows?:
volumebtn_sethandler_sig(btn["VOL-"], "VOL-", env)
volumebtn_sethandler_sig(btn["VOL+"], "VOL+", env)

#Directly perform actions (don't trigger a signal that first needs to be trapped):
#-------------------------------------------------------------------------------
#NOTE: By sending signals, environment could be configured with traps that reduce volume (instead of actually muting).
volumebtn_sethandler(btn["mute"], Action_VolumeMute("MASTER", 1), env)
volumebtn_sethandler(btn["un-mute"], Action_VolumeMute("MASTER", 0), env)
volumebtn_sethandler(btn["toggle mute"], Action_VolumeMute("MASTER"), env)


#==Show/start application
#===============================================================================
appwnd.mainloop()