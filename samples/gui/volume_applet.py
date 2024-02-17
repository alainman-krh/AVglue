#samples/gui/volume_applet.py
#-------------------------------------------------------------------------------
from AVglue.Windows.Actions import *
from AVglue.Actions import *
from AVglue.PythonTools import clamp2range
from PySystemDefs import MediaPC1
from TKglue.EventHandling import wgt_sethandler
import tkinter as tk


#==Fancy volume scrubber
#===============================================================================
class VolumeScrubber:
	"""Wrapper class to handle complexity of tk.Scrollbar"""
	def __init__(self, parent, env):
		self.w = tk.Scrollbar(parent, orient="horizontal")
		self.env = env
		self.wbox = 0.2 #With of scrollbox
		self.w.pack(fill="x")
		self.valrange = (-30.0, 0.0) #dB (float)
		self._scrubhandler_set()
		self.pagestep = 3.0 #dB (float)
		self.refresh()

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
appwnd.title("Volume control")
btn = {}

#First row: volume scrollbar
#-------------------------------------------------------------------------------
volscrub = VolumeScrubber(appwnd, env)

#Define `Frame`s used to place buttons in rows
#-------------------------------------------------------------------------------
NROWS = 5
frame_rows = [
	tk.Frame(appwnd) for i in range(NROWS)
]
for f in frame_rows:
	f.pack()

#Add mode buttons
#-------------------------------------------------------------------------------
fref = frame_rows[0]
frame_rows[0].pack(fill="both", expand=True)
for id in ("mode: volumectrl", "mode: notepad"):
	btn[id] = tk.Button(fref, text=id)
	btn[id].pack(side="left", fill="both", expand=True)

#Add numbered buttons (volume presets)
#-------------------------------------------------------------------------------
fref = frame_rows[1]
for i in (*range(1, 10), 0): #Want 0 last
	btn[i] = tk.Button(fref, text=f"     {i}     ")
	btn[i].pack(side="left", fill="y")
	if 5==i:
		fref = frame_rows[2]

#Add volume -/+ buttons
#-------------------------------------------------------------------------------
fref = frame_rows[3]
for id in ("VOL-", "VOL+"):
	btn[id] = tk.Button(fref, text=id)
	btn[id].pack(side="left", fill="y")

#Add mute buttons
#-------------------------------------------------------------------------------
fref = frame_rows[4]
for id in ("mute", "un-mute", "toggle mute"):
	btn[id] = tk.Button(fref, text=id)
	btn[id].pack(side="left", fill="y")


#==Connect appropriate event handlers
#===============================================================================

#Mode select
#-------------------------------------------------------------------------------
def EHmodesel_click(btn:tk.Button, env:OperatingEnvironment):
	if "notepad" in btn["text"]:
		success = Action_TriggerLocal(Signal("MODENOTEPAD")).run(env)
		if not success: #TODO: Won't work because can't yet detect application isn't present.
			print("Please ensure there is a running copy of notepad with the following")
			print('window title: "Untitled - Notepad"')
	else:
		env.signal_trigger(Signal("MODEVOL"))
for id in ("mode: volumectrl", "mode: notepad"):
	wgt_sethandler(btn[id], EHmodesel_click, env)

#Number buttons: Send NUMBTN signals
#-------------------------------------------------------------------------------
def EHnumbuttons_click(btn:tk.Button, env:OperatingEnvironment):
	num = int(btn["text"])
	env.signal_trigger(Signal("NUMBTN"), data_int64=num)
	volscrub.refresh() #Don't forget to refresh GUI when you run an action!
for i in range(10): #0-9
	wgt_sethandler(btn[i], EHnumbuttons_click, env)

#"VOL-/+": Send signals instead of running actions directly!
#(Maybe user wants the signal traps prefer to jump up/down by 1, 2, 3 steps... who knows?)
#...or maybe user wants volume -/+ to only work in certain modes
#-------------------------------------------------------------------------------
def EHvolupdn_click(btn:tk.Button, env:OperatingEnvironment):
	sigmap = { #Technically don't need a map here - but useful pattern:
		"VOL-": Signal("VOL-"),
		"VOL+": Signal("VOL+"),
	}
	signal = sigmap[btn["text"]]
	success = env.signal_trigger(signal)
	if not success:
		print('Switch back to "mode: volumectrl" to trap signals')
	volscrub.refresh() #Don't forget to refresh GUI when you run an action!
for id in ("VOL-", "VOL+"):
	wgt_sethandler(btn[id], EHvolupdn_click, env)

#Mute/un-mute: Directly perform actions (don't trigger a signal that first needs to be trapped):
#HOWEVER: By sending signals, environment could be configured with traps that reduce volume (instead of actually muting).
#-------------------------------------------------------------------------------
def EHvolmute_click(btn:tk.Button, env):
	muteop = 1 #basic mute
	lbl = btn["text"]
	if "un-" in lbl:
		muteop = 0 #unmute
	elif "toggle" in lbl:
		muteop = -1
	success = Action_VolumeMute("MASTER", muteop).run(env)
	volscrub.refresh() #Don't forget to refresh GUI when you run an action!
for id in ("mute", "un-mute", "toggle mute"):
	wgt_sethandler(btn[id], EHvolmute_click, env)


#==Show/start application
#===============================================================================
appwnd.mainloop()