#AVglue/Listener.py
#-------------------------------------------------------------------------------
import socket

DFLT_RX_MAXCHUNK = 1024


#==Line 
#===============================================================================
class SocketMessageReceiver():
	"""Decodes incomming messages"""
	def __init__(self, maxchunk=DFLT_RX_MAXCHUNK):
		self.maxchunk = maxchunk #TODO: Use same buffer
		self.buf = "" #Nothing

	def _buf_popmsg(self):
		"""Removes contents of self.buf - and returns it."""
		msg = self.buf
		self.buf = ""
		return msg

	def _buf_readmsg(self):
		msgend = self.buf.find("\n")
		if msgend >= 0:
			msg = self.buf[:msgend]
			self.buf = self.buf[msgend+1:]
			return msg
		return None

	def readline(self, com:socket.socket):
		msg = self._buf_readmsg()
		if msg != None:
			return msg
		
		while True:
			chunk = com.recv(self.maxchunk)
			if b"" == chunk:
				if len(self.buf) > 0:
					return self._buf_popmsg()
				else:
					return None #Indicate socket disconnection
			self.buf += chunk.decode("utf-8")
			msg = self._buf_readmsg()
			if msg != None:
				return msg
