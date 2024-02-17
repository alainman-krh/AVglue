#samples/gui/volume_applet.py
#-------------------------------------------------------------------------------
from AVglue.Windows.Actions import *
from AVglue.Actions import *
from AVglue.PythonTools import clamp2range
from PySystemDefs import MediaPC1
from TKglue.Builders import TKButtonRows, SEP_ROW
import tkinter as tk


#Alias to AVGlue.OperatingEnvironment:
env = MediaPC1.env


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


#==Event handlers
#===============================================================================

#Mode select
#-------------------------------------------------------------------------------
def EHmodesel_click(btn:tk.Button, env:OperatingEnvironment):
	if "notepad" in btn.btnid:
		success = Action_TriggerLocal(Signal("MODENOTEPAD")).run(env)
		if not success: #TODO: Won't work because can't yet detect application isn't present.
			print("Please ensure there is a running copy of notepad with the following")
			print('window title: "Untitled - Notepad"')
	else:
		env.signal_trigger(Signal("MODEVOL"))

#Number buttons: Send NUMBTN signals
#-------------------------------------------------------------------------------
def EHnumbuttons_click(btn:tk.Button, env:OperatingEnvironment):
	num = int(btn.btnid)
	env.signal_trigger(Signal("NUMBTN"), data_int64=num)
	volscrub.refresh() #Don't forget to refresh GUI when you run an action!

#"VOL-/+": Send signals instead of running actions directly!
#(Maybe user wants the signal traps prefer to jump up/down by 1, 2, 3 steps... who knows?)
#...or maybe user wants volume -/+ to only work in certain modes
#-------------------------------------------------------------------------------
def EHvolupdn_click(btn:tk.Button, env:OperatingEnvironment):
	sigmap = { #Technically don't need a map here - but useful pattern shown as an example:
		"VOL-": Signal("VOL-"),
		"VOL+": Signal("VOL+"),
	}
	signal = sigmap[btn.btnid]
	success = env.signal_trigger(signal)
	if not success:
		print('Switch back to "mode: volumectrl" to trap signals')
	volscrub.refresh() #Don't forget to refresh GUI when you run an action!

#Mute/un-mute: Directly perform actions (don't trigger a signal that first needs to be trapped):
#HOWEVER: By sending signals, environment could be configured with traps that reduce volume (instead of actually muting).
#-------------------------------------------------------------------------------
def EHvolmute_click(btn:tk.Button, env):
	muteop = 1 #basic mute
	if "un-" in btn.btnid:
		muteop = 0 #unmute
	elif "toggle" in btn.btnid:
		muteop = -1
	success = Action_VolumeMute("MASTER", muteop).run(env)
	volscrub.refresh() #Don't forget to refresh GUI when you run an action!


#==Build up GUI
#===============================================================================
appwnd = tk.Tk()  # create parent window
appwnd.title("Volume control")
rows_mode = TKButtonRows(appwnd) #Separate one - just for modes
rowsi = TKButtonRows(appwnd) #All other rows in here

#+ROW: volume scrollbar
#-------------------------------------------------------------------------------
volscrub = VolumeScrubber(appwnd, env)

#+ROW: mode buttons
#-------------------------------------------------------------------------------
modebtn_lblmap = {
	"mode:volctrl": "Mode: Volume control",
	"mode:notepad": "Mode: Notepad write",
}
rows_mode.row_append(fill="both", expand=True)
rows_mode.btnpack_change(side="left", fill="both", expand=True)
rows_mode.createblock(modebtn_lblmap, EHmodesel_click, data=env)

#+ROW: numbered buttons (volume presets)
#-------------------------------------------------------------------------------
numbtn_list = tuple(range(10))
numbtn_lblmap = {f"{i}": f"     {i}     " for i in numbtn_list}
numbtn_lyt = ["1", "2", "3", "4", "5", SEP_ROW, "6", "7", "8", "9", "0"]
rowsi.row_append(2)
rowsi.createblock(numbtn_lblmap, EHnumbuttons_click, data=env, layout=numbtn_lyt)

#+ROW: volume -/+ buttons
#-------------------------------------------------------------------------------
volbtn_map = {"VOL-": "VOL-", "VOL+": "VOL+"}
rowsi.row_append()
rowsi.createblock(volbtn_map, EHvolupdn_click, data=env)

#Add mute buttons
#-------------------------------------------------------------------------------
mutebtn_list = ("mute", "un-mute", "toggle mute")
mutebtn_map = {id: id for id in mutebtn_list}
rowsi.row_append()
rowsi.createblock(mutebtn_map, EHvolmute_click, data=env)


#==Show/start application
#===============================================================================
appwnd.mainloop()