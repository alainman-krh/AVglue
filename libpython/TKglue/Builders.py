#TKglue/Builders.py
#-------------------------------------------------------------------------------
import tkinter as tk
from .EventHandling import wgt_sethandler

SEP_ROW = "-" #String/object used to identify a row separator


#==TKButtonRows
#===============================================================================
class TKButtonRows:
	def __init__(self, parent):
		self.nrows = 0
		self.parent = parent

	def append(self, nrows):
		self.nrows += nrows
		self.frame_rows = [
			tk.Frame(self.parent) for i in range(nrows)
		]
		for f in self.frame_rows:
			f.pack(fill="y") #Add elements from left-to-right
		return

	def createblock(self, lblmap:dict, wgtlayout:list, fnEHandler, data=None, rowstart=0):
		"""-fnEHandler: Event handler function with arguments: (btn:tk.Button, data)"""
		row = rowstart
		for key in wgtlayout:
			if key == SEP_ROW:
				row += 1
				continue
			lbl = lblmap[key]
			btn = tk.Button(self.frame_rows[row], text=lbl)
			btn.btnid = key #Add signame property to button
			wgt_sethandler(btn, fnEHandler, data)
			btn.pack(side="left")
