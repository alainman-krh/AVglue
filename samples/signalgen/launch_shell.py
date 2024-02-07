#samples/signalgen/launch_shell.py
#-------------------------------------------------------------------------------
from os.path import join as joinpath
from os.path import basename, dirname, abspath
import os
_THIS_FILE = abspath(__file__)
_THIS_DIR = dirname(_THIS_FILE)

#Add ../libpython to PYTHONPATH - and execute python version used to run this code right here:
_THIS_LIBDIR = abspath(joinpath(_THIS_DIR, "..", "..", "libpython"))

print("Launching shell terminal (Windows PC)")
print("run `python signal_send.py` to send a signal to a running AVglue listener.")
print("(ex: ../mediapc1_listener.py).")
os.chdir(_THIS_DIR)
os.system("start powershell")
