#AVglue/SocketSignals.py
#-------------------------------------------------------------------------------
from .Base import OperatingEnvironment, Signal
from .Actions import Action_TriggerLocal
from .SocketsBase import SocketMessageReceiver
from abc import ABCMeta, abstractmethod
import socket

DFLT_PORT_CONNECTIONMGR = 50042


#==Exeptions
#===============================================================================
class TerminationRequest(Exception):
	"""TODO: Implement? Not sure this is required. Intent: Detect a `Signal("TERM")` - or something and throw exception/exit"""
	pass


#==Worker classes (listener/server side)
#===============================================================================
class AbstractWorker(metaclass=ABCMeta):
	"""Mostly used to identify class as a worker (listener/server side)"""
	pass

class SignalListener(AbstractWorker):
	def __init__(self, verbose=False):
		super().__init__()
		self.rxbuf = SocketMessageReceiver()
		self.verbose = verbose

	def message_process(self, env:OperatingEnvironment, msg:str):
		tokens = msg.split()
		N = len(tokens)
		data = None
		if not (1 <= N <= 2):
			env.log_error("Only support signals with 1 optional argument")
			return
		elif N > 1:
			dstr = tokens[1]
			if "0x" == dstr[:2]:
				data = int(dstr, 16)
			else:
				data = int(dstr)

		id = tokens[0]
		act = Action_TriggerLocal(Signal(id), data_int64=data)
		if self.verbose:
			env.log_info(f"Running action: {act.serialize()}.")
		act.run(env)

	def run(self, env:OperatingEnvironment, client:socket.socket):
		while True:
			msg = self.rxbuf.readline(client)
			if msg is None:
				return
			self.message_process(env, msg)


#==Worker class
#===============================================================================
class ConnectionManager():
	"""Listener (Server) side."""
	def __init__(self, env, port=DFLT_PORT_CONNECTIONMGR):
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