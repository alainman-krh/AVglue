# config_py: Hack to access submodules of ../config_py (normally can't go up beyond applet "root" folder)
#-------------------------------------------------------------------------------
from os.path import join as joinpath
from os.path import basename, dirname, abspath
from AVglue.PythonTools import add_module_direct
_THIS_DIR = dirname(abspath(__file__))
IMPORTDIR = joinpath(_THIS_DIR, "..", "config_py")

#Provide module references:
MediaPC1 = add_module_direct(joinpath(IMPORTDIR, "MediaPC1.py"), register=False)