#AVglue/launcher/buildlauncher_windows.py
#-------------------------------------------------------------------------------
from os.path import join as joinpath
from os.path import basename, dirname, abspath
import sys
_THIS_FILE = abspath(__file__)
_THIS_DIR = dirname(_THIS_FILE)

#Add ../libpython to PYTHONPATH - and execute python version used to run this code right here:
_THIS_LIBDIR = abspath(joinpath(_THIS_DIR, "..", "libpython"))
_THIS_LAUNCHSCRIPT = abspath(joinpath(_THIS_DIR, "..", "samples", "usage_basic.py"))
_THIS_PYTHON = sys.executable

launch_script = f"""'AVglue launcher
Set shell = CreateObject("WScript.shell")
Set sysenv = shell.Environment("Process")
sysenv("PYTHONPATH") = "{_THIS_LIBDIR}"

shell.Run "{_THIS_PYTHON} {_THIS_LAUNCHSCRIPT}"
"""

with open("AVglue.vbs", "w") as io:
    print(launch_script, file=io)