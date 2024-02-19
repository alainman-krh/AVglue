#SerialGlue/LossyMessaging.py: "Immediate-mode" messaging (keeps last message only)
#-------------------------------------------------------------------------------
from serial import Serial
from time import time as time_now

r"""
For use when signals are human generated (ex: operating an IR remote).

With human-generated signalling: you don't want to queue up all messages and execute
them. Often: there will be undesired repeats - and possibly glitches due to interference
or moving signal source, etc.

Assumptions (think IR remote operated by a human):
- Messages are (potentially) repetedly sent because link/medium is unreliable.
- Mis-detections/glitches are likely to occur due to link/medium reliability issues.

- clear before read.
- Accum: 5 signals repeated.
- wait preiod of quiet time

TEST:
- How many signals recieved when processing
"""

class LossySerial:
	"""Basically "de-bounces" incomming messages"""
	def __init__(self, com:Serial, mingap=0.1, timeout=0.2):
		"""!Warning!: changes `com.timeout` value."""
		self.com = com
		self.lastmsg_detected = None
		self.lastmsg_timestamp = time_now()
		self.minrepeat = 3 #Number of repeated detections before message is considered "detected".
		self.timeout_set(timeout, mingap)
		self.verbose = False

	def timeout_set(self, timeout, mingap=0):
		if mingap < timeout: #Not practical
			mingap = timeout
		self.mingap = mingap #Minimum timespan (sec) needed between messages to register as a new "detection" (human timescales).
		self.com.timeout = timeout #Can be read

	def readline(self):
		rpt = 0 #Number of repeated signals
		now = time_now()
		deltaT = now - self.lastmsg_timestamp
		lastmsg = None; lastmsg_timestamp = now
		if deltaT > self.mingap:
			self.com.reset_input_buffer() #Assume whatever was missed since last capture is irrelevant.
			self.lastmsg_detected = None
		else: #Continue from where we were:
			lastmsg = self.lastmsg_detected
			lastmsg_timestamp = self.lastmsg_timestamp
			rpt = self.minrepeat # Next similar signal is considered "detected"

		while True:
			#N1 = com.in_waiting #no of bytes in buffer
			msg = self.com.readline() #.decode("utf-8")
			now = time_now()
			if b"" == msg: #Still want to return if timed out (avoid blocking thread).
				#Don't NEED to reach self.minrepeat. Single detect+timeout is ok!:
				if lastmsg != None:
					self.lastmsg_detected = lastmsg
					self.lastmsg_timestamp = lastmsg_timestamp
				return lastmsg
			elif msg == lastmsg:
				rpt += 1
				if rpt >= self.minrepeat:
					self.lastmsg_detected = msg
					self.lastmsg_timestamp = now
					return msg
			else:
				#Maybe last message was a glitch... reset
				lastmsg = msg
				lastmsg_timestamp = now
				rpt = 0

