#samples/mediapc1_listener.py
#-------------------------------------------------------------------------------
from config_py import MedaPC1 #Assume current folder is in path
from AVglue.Listener import SocketListener

slist = SocketListener(MedaPC1.env)
slist.start(verbose=True)

print("Done")
# Last line