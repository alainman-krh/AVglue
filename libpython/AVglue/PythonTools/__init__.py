#AVglue/PythonTools
from os.path import basename, dirname, abspath, splitext
from os.path import join as joinpath
import importlib.util as importutil
import sys


#==Module utilities
#===============================================================================
def add_module_direct(modulepath, register=True):
	modulepath = abspath(modulepath)
	modulename = splitext(basename(modulepath))[0]
	spec = importutil.spec_from_file_location(modulename, modulepath)
	module = importutil.module_from_spec(spec)
	spec.loader.exec_module(module)
	if register:
		sys.modules[modulename] = module
	return module


#==Math
#===============================================================================
def clamp2range(rng:tuple, v):
	_min = min(rng); _max = max(rng)
	return max(_min, min(_max, v))
