#AVglue/applets/build/buildlauncher_AVglue_send.py
#-------------------------------------------------------------------------------
from os.path import join as joinpath
from os.path import basename, dirname, abspath
import sys
_THIS_FILE = abspath(__file__)
_THIS_DIR = dirname(_THIS_FILE)
_THIS_PYTHON = sys.executable

cmd_name = "AVglue_send"

#Add ../libpython to PYTHONPATH - and execute python version used to run this code right here:
ROOTDIR_AVGLUE = abspath(joinpath(_THIS_DIR, "..", ".."))
LIBDIR_AVGLUE = joinpath(ROOTDIR_AVGLUE, "libpython")
APPLETDIR = joinpath(ROOTDIR_AVGLUE, "applets", "Windows")
LAUNCHSCRIPT_VBSWRAP = joinpath(APPLETDIR, cmd_name + ".vbs") #.vbs wrapper
LAUNCHSCRIPT_PYTHON = joinpath(APPLETDIR, "src", cmd_name + ".py") #Actual script
PYTHONCMD = joinpath(dirname(_THIS_PYTHON), "pythonw.exe") #Use pythonw. Doesn't use console mode
#PYTHONCMD = _THIS_PYTHON

launch_script = f"""'{cmd_name}.vbs
Set shell = CreateObject("WScript.Shell")
shell.Environment("Process")("PYTHONPATH") = "{LIBDIR_AVGLUE}"
cmd = "{PYTHONCMD} {LAUNCHSCRIPT_PYTHON}"
For Each arg In WScript.Arguments
    cmd = cmd & " " & arg
Next
'WScript.Echo cmd
shell.Run cmd
"""

with open(LAUNCHSCRIPT_VBSWRAP, "w") as io:
    print(launch_script, file=io)