#TKglue/EventHandling.py
#-------------------------------------------------------------------------------
import tkinter as tk


#==Register event handlers
#===============================================================================
def wgt_sethandler(wgt:tk.Widget, fn_eventhandler, data):
	"""Set widget event handler to run a particular action
	- data: Some extra data to be provided to event handler
	"""
	#NOTE: lambda uses variables with local scope here - so we know that
	#whatever arguments are passed to this function will exist only for this
	#one event handler/lambda function (safe/works).
	wgt.configure(command=lambda : fn_eventhandler(wgt, data))

def wgtdict_findkey_matching(wgt:tk.Widget, wgtdict):
	"""-wgtlist:tk.Widget[]"""
	for (k, w) in wgtdict.items():
		if w is wgt:
			return k
	return None
