#TKglue/EventHandling
#-------------------------------------------------------------------------------
from AVglue.Base import AbstractAction, Signal
from AVglue.Actions import Action_TriggerLocal
import tkinter as tk


#==Register event handlers
#===============================================================================
def wgt_sethandler(wgt:tk.Widget, fn_eventhandler, env):
	"""Set widget event handler to run a particular action"""
	#NOTE: lambda uses variables with local scope here - so we know that
	#whatever arguments are passed to this function will exist only for this
	#one event handler/lambda function (safe/works).
	wgt.configure(command=lambda : fn_eventhandler(wgt, env))
