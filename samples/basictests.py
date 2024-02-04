from AVglue.Base import OperatingEnvironment
from AVglue.Actions import *

env = OperatingEnvironment()

act_calcopen = Action_ExecuteShell("calc.exe")
#act_calcopen.run(env)


act_dothething = Action_ExecuteSequence("CALCTEST", [
    Action_ExecuteShell("calc.exe"),
    Action_Wait(0.5),
    Action_SendKeys(0, "3{+}14{ENTER}"),
])

act_dothething.run(env)