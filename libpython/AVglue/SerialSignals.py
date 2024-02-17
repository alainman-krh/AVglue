#AVglue/SerialSignals.py
#-------------------------------------------------------------------------------
from .Base import OperatingEnvironment, AbstractWorker
from serial import Serial


#==Worker classes (listener/server side)
#===============================================================================
class SignalListener(AbstractWorker):
	def __init__(self, verbose=False):
		super().__init__()
		self.verbose = verbose

	def run(self, env:OperatingEnvironment, io:Serial):
		while True:
			msg = io.readline()
			if msg is None:
				return
			env.message_process(msg)

#TODO: Make a listener that runs in a separate thread, and indirectly informs main thread that a signal exists


#==ConnectionManager (listener/server side)
#===============================================================================
class ConnectionManager():
	"""Listener (server) side."""
	def __init__(self, env):
		self.env = env

	def start(self, port:str, verbose=False):
		io = Serial(port)
		self.env.log_info(f"Connected to {port}.")

		with io:
			while True:
				worker = SignalListener(verbose=verbose)
				worker.run(self.env, io)
				#break #Make self available for new connections
