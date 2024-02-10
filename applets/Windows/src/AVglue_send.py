#AVglue/launcher/Windows/AVglue_send.py
#-------------------------------------------------------------------------------
#NOTE: Need to setup PYTHONPATH and use python.exe from correct environment.
from AVglue.SocketSignals import DFLT_PORT_CONNECTIONMGR
from sys import argv
import socket

host = "127.0.0.1" #Talk to local listener
port = DFLT_PORT_CONNECTIONMGR #Assume listener uses this port
#port = 50043 #Try a different port
msg = " ".join(argv[1:])

#print(f"Connection to {host}:{port}...") #DEBUG
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

msgb = (msg+"\n").encode("UTF-8") #Protocol expects `\n`
sock.sendall(msgb)
# Last line