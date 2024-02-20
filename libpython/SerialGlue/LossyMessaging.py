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
"""

r"""Useful code
- N1 = com.in_waiting #number of of bytes in buffer
"""


#==LossySerial
#===============================================================================
class LossySerial:
	"""Basically "de-bounces" incomming messages"""
	def __init__(self, com:Serial, ignore_repeats=False, mingap=0.1, timeout=0):
		"""!Warning!: changes `com.timeout` value."""
		self.com = com
		self.lastmsg_detected = None
		self.lastmsg_timestamp = time_now()
		#self.minrepeat = 3 #Number of repeated detections before message is considered "detected".
		self.minrepeat = 0 #Don't "debounce": NEC protocol only sends a single actual signal (followed by repeats)
		self.ignore_repeats = ignore_repeats
		self.timeout_set(timeout, mingap)
		self.verbose = False

	def timeout_set(self, timeout, mingap=0):
		if timeout <= 0:
			timeout = None
			mingap = max(0, mingap)
		elif mingap < timeout: #Not practical
			mingap = timeout
		self.mingap = mingap #Minimum timespan (sec) needed between messages to register as a new "detection" (human timescales).
		self.com.timeout = timeout #Can be read

	def reset_input_buffer(self):
		self.com.reset_input_buffer() #Assume whatever was missed since last capture is irrelevant.
		self.lastmsg_detected = None

	def _lastmsg_update_maskrep(self, lastmsg, timestamp):
		"""Update last message and mask repeats"""
		first_sent = (lastmsg == self.lastmsg_detected)
		self.lastmsg_timestamp = timestamp #Update timestamp no matter what
		self.lastmsg_detected = lastmsg
		if first_sent and self.ignore_repeats:
			return None #Mask repeats... but still update timestamp!
		return lastmsg

	def readline(self):
		rpt_left = self.minrepeat
		now = time_now()
		deltaT = now - self.lastmsg_timestamp
		if deltaT > self.mingap:
			self.reset_input_buffer()
		elif self.lastmsg_detected != None:
			#Continue from where we were:
			rpt_left = 0 #Next signal matching `lastmsg_detected` again is considered "detected"

		lastmsg = self.lastmsg_detected
		lastmsg_thisrun = None
		lastmsg_timestamp = self.lastmsg_timestamp
		while True:
			msg = self.com.readline() #.decode("utf-8")
			#print("BEEP") #DEBUG
			now = time_now()
			deltaT = now - lastmsg_timestamp
			if b"" == msg: #Still want to return if timed out (avoid blocking thread).
				#Don't NEED to reach self.minrepeat. Single detect(lastmsg)+timeout is ok!:
				#print("deltaT", deltaT)
				#Possibly "detected":
				return self._lastmsg_update_maskrep(lastmsg_thisrun, lastmsg_timestamp)
			elif deltaT > self.mingap:
				if lastmsg_thisrun is None: #Actually the first message we caught...
					#...let's wait for the repeats (don't return right away):
					self.lastmsg_detected = None #Assume there was no previous message sent (new btn; not repeat)
					lastmsg = msg
					lastmsg_thisrun = msg
					lastmsg_timestamp = now
					rpt_left = self.minrepeat
				else:
					#"detect" `lastmsg` first... we'll catch repeats of this message later on:
					#If self.lastmsg_detected... keep it. This one counts as a repeat
					return self._lastmsg_update_maskrep(lastmsg_thisrun, lastmsg_timestamp)
			elif (msg == lastmsg):
				lastmsg_timestamp = now
				rpt_left -= 1
			else:
				#Maybe last message was a glitch... reset
				lastmsg = msg
				lastmsg_thisrun = msg
				lastmsg_timestamp = now
				rpt_left = self.minrepeat

			if rpt_left <= 0:
				#Possibly "detected" (if !ignore_repeats):
				return self._lastmsg_update_maskrep(msg, now)

#Last line