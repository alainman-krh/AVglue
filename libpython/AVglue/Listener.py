#AVglue/Listener.py
#-------------------------------------------------------------------------------
from .Base import OperatingEnvironment, Signal
from .Actions import Action_TriggerLocal
from .SocketsBase import SocketMessageReceiver
from abc import ABCMeta, abstractmethod
import socket

DFLT_PORT_LISTENER = 50042


#==Worker class
#===============================================================================
class AbstractWorker(metaclass=ABCMeta):
	"""Mostly used to identify class"""
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
class SocketListener():
	def __init__(self, env, port=DFLT_PORT_LISTENER):
		self.env = env
		self.port = port

	def start(self, verbose=False):
		lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#host = socket.gethostname()
		host = "127.0.0.1"
		lsock.bind((host, self.port))
		self.env.log_info(f"Listening for connections to {host}:{self.port}.")

		lsock.listen(1) #1 connection at a time
		while True:
			(client, addr) = lsock.accept()
			print(addr)
			with client:
				worker = SignalListener(verbose=verbose)
				worker.run(self.env, client)
			break