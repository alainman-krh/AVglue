#samples/signalgen/launch_shell.py
#-------------------------------------------------------------------------------
from os.path import join as joinpath
from os.path import basename, dirname, abspath
import os, sys
_THIS_FILE = abspath(__file__)
_THIS_DIR = dirname(_THIS_FILE)
CMD_PYTHON = sys.executable #Need full path when starting powershell

#Add ../libpython to PYTHONPATH - and execute python version used to run this code right here:
_THIS_LIBDIR = abspath(joinpath(_THIS_DIR, "..", "..", "libpython")) #Already in PYTHONPATH (if running from properly setup VSCODE)
#...And `python` should also be in path

scriptpath = joinpath(_THIS_DIR, "mediapc1_listener.py")

cmd = f"python {scriptpath}"
cmd = f"{CMD_PYTHON} {scriptpath}"
#cmd = None

os.chdir(_THIS_DIR)
if cmd is None:
    print("Launching shell terminal (Windows PC)")
    print("run `python signal_send.py` to send a signal to a running AVglue listener.")
    print("(ex: ../mediapc1_listener.py).")
    os.system("start powershell")
else:
    print(f"Running `{cmd}`...")
    os.system(f'start powershell -Command "{cmd}; pause"')
    #os.system(cmd)
