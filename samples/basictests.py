from AVglue.Actions import *

act_calcopen = Action_ExecuteShell("calc.exe")
#act_calcopen.run()


act_dothething = Action_ExecuteSequence([
    Action_ExecuteShell("calc.exe"),
    Action_Wait(0.5),
    Action_SendKeys(0, "3{+}14{ENTER}"),
])
act_dothething.run()