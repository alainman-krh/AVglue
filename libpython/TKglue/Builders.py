#TKglue/Builders.py
#-------------------------------------------------------------------------------
import tkinter as tk
from .EventHandling import wgt_sethandler

SEP_ROW = "-" #String/object used to identify a row separator


#==TKButtonRows
#===============================================================================
class TKButtonRows:
	def __init__(self, parent):
		self.parent = parent
		self.frame_rows = []
		self.rowstart_default = 0
		self.btnpack_change(side="left") #Add elements from left-to-right

	def btnpack_change(self, **opts):
		"""Chage ".pack()" options for future calls to .createblock()."""
		self.opts_btnpack = opts

	def row_append(self, nrows=1, **packopt):
		if len(packopt) < 1:
			packopt = {"fill": "y"}
		self.rowstart_default = len(self.frame_rows)
		rows_new = [tk.Frame(self.parent) for i in range(nrows)]
		self.frame_rows.extend(rows_new)
		for f in rows_new:
			f.pack(**packopt)
		return

	def createblock(self, lblmap:dict, fnEHandler, data=None, layout:list=None, rowstart=None):
		"""-fnEHandler: Event handler function with arguments: (btn:tk.Button, data)"""
		if layout is None:
			layout = lblmap.keys() #`dict`s are ordered - and have been for a while
		if rowstart is None:
			rowstart = self.rowstart_default
		row = rowstart
		for key in layout:
			if key == SEP_ROW:
				row += 1
				continue
			lbl = lblmap[key]
			btn = tk.Button(self.frame_rows[row], text=lbl)
			btn.btnid = key #Add signame property to button
			wgt_sethandler(btn, fnEHandler, data)
			btn.pack(**self.opts_btnpack)
