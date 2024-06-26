#samples/mediapc1_test.py
#-------------------------------------------------------------------------------
from PySystemDefs import MediaPC1 #Assume current folder is in path
from AVglue.Actions import *
from AVglue.Windows.Actions import *

act_mediatest = Action_ExecuteSequence("DEPRECATEIDFIELD?", [
	Action_TriggerLocal(Signal("VOLMUTE")),
	Action_TriggerLocal(Signal("VOLMUTEX")),
	Action_TriggerLocal(Signal("IRNEC"), data_int64=0xABCD123), #Not obvious what data is - will get decoded
	Action_TriggerLocal(Signal("NUMBTN"), data_int64=0xABCD),
	Action_TriggerLocal(Signal("NUMBTN"), data_int64=5), #Volume apply preset 5
	Action_TriggerLocal(Signal("NUMBTN"), data_int64=100), #Volume down
	Action_LogString("COMPLETE!"),
])
success = act_mediatest.run(MediaPC1.env)
