#samples/mediapc1_listener.py
#-------------------------------------------------------------------------------
from config_py import MedaPC1 #Assume current folder is in path
from AVglue.SocketSignals import ConnectionManager

r"""IMPORTANT
PLEASE RUN IN A SEPARATE THREAD (using `./1-launch_listener.py`)
"""

slist = ConnectionManager(MedaPC1.env)
slist.start(verbose=True)

print("Done")
# Last line