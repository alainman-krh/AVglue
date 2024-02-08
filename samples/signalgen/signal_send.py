#samples/signalgen/signal_send.py
#-------------------------------------------------------------------------------
#NOTE: Launch from spearate command window with python environment ready
from AVglue.SocketSignals import DFLT_PORT_CONNECTIONMGR
import socket
from time import sleep

#Assume this is where listener is:
host = "127.0.0.1"
port = DFLT_PORT_CONNECTIONMGR
#port = 50043 #Try a different port
msg = "VOLMUTE"

print(f"Connection to {host}:{port}...")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

msgb = (msg+"\n").encode("UTF-8") #Protocol expects `\n`
sock.sendall(msgb)
#sleep(5)
#sock.sendall(msgb)

print("Done")
# Last line