#samples/mediapc1_listener.py
#-------------------------------------------------------------------------------
from PySystemDefs import MediaPC1 #Assume current folder is in path
from AVglue.SocketSignals import ConnectionManager

r"""IMPORTANT
PLEASE RUN IN A SEPARATE THREAD (suggest using `./1-launch_listener.py`)
"""

slist = ConnectionManager(MediaPC1.env)
slist.start(verbose=True)

print("Done")
# Last line