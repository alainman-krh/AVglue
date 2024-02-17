#AVglue/SocketSignals.py
#-------------------------------------------------------------------------------
from .Base import OperatingEnvironment, AbstractWorker
from .SocketsBase import SocketMessageReceiver
import socket

DFLT_PORT_CONNECTIONMGR = 50042


#==Exeptions
#===============================================================================
class TerminationRequest(Exception):
	"""TODO: Implement? Not sure this is required. Intent: Detect a `Signal("TERM")` - or something and throw exception/exit"""
	pass


#==Worker classes (listener/server side)
#===============================================================================
class SignalListener(AbstractWorker):
	def __init__(self, verbose=False):
		super().__init__()
		self.rxbuf = SocketMessageReceiver()
		self.verbose = verbose

	def run(self, env:OperatingEnvironment, client:socket.socket):
		while True:
			msg = self.rxbuf.readline(client)
			if msg is None:
				return
			env.message_process(msg)


#==ConnectionManager (listener/server side)
#===============================================================================
class ConnectionManager():
	"""Listener (server) side."""
	def __init__(self, env):
		self.env = env

	def start(self, port=DFLT_PORT_CONNECTIONMGR, verbose=False):
		#Listener socket
		lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#host = socket.gethostname()
		host = "127.0.0.1"
		lsock.bind((host, port))
		self.env.log_info(f"Listening for connections to {host}:{port}.")

		while True:
			lsock.listen(1) #1 connection at a time

			(client, addr) = lsock.accept()
			self.env.log_info(f"New connection: {addr}.")
			with client:
				worker = SignalListener(verbose=verbose)
				worker.run(self.env, client)
			#break #Make self available for new connections