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

	def _readmsg(self, buf):
		msgend = buf.find("\n")
		if msgend >= 0:
			msg = buf[:msgend]
			buf = buf[msgend+1:]
			return msg
		return None

	def readline(self, com:socket.socket):
		msg = self._readmsg(self.buf)
		if msg != None:
			return msg
		
		while True:
			chunk = com.recv(self.maxchunk)
			if b"" == chunk:
				if len(self.buf) > 0:
					return self.buf
				else:
					return None #Indicate socket disconnection
			self.buf += chunk.decode("utf-8")
			msg = self._readmsg(self.buf)
			if msg != None:
				return msg
