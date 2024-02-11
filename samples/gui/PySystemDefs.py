#PySystemDefs.py: Hack to access submodules of ../PySystemDefs.py
#-------------------------------------------------------------------------------
#(normally can't go up beyond "root" folder of the applet)
from os.path import join as joinpath
from os.path import basename, dirname, abspath
from AVglue.PythonTools import add_module_direct
_THIS_DIR = dirname(abspath(__file__))
IMPORTDIR = joinpath(_THIS_DIR, "..", "PySystemDefs")

#Provide module references:
MediaPC1 = add_module_direct(joinpath(IMPORTDIR, "MediaPC1.py"), register=False)