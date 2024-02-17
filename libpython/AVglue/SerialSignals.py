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
	def __init__(self, env, io=None):
		self.env = env
		self.io = io

	def ensure_connected(self, want_connected):
		if want_connected:
			if self.io is None:
				raise Exception("Cannot proceed: not connected!")
		else:
			if self.io != None:
				raise Exception("Cannot proceed: already connected!")

	def connect(self, port):
		self.ensure_connected(False)
		self.io = Serial(port)

	def start(self, connect=None, verbose=False):
		if connect != None:
			self.connect(port=connect)
		self.ensure_connected(True)
		self.env.log_info(f"Connected to {self.io}.")
		print(self.io.name)
		with self.io:
			while True:

				worker = SignalListener(verbose=verbose)
				worker.run(self.env, self.io)
				#break #Make self available for new connections
	