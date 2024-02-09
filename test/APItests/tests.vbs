'Aliases: WScript, WSH, wsh
'- Running from wscript [filename.vbs] will run in windows (graphical) mode.
'- Running from cscript [filename.vbs] will run in a console.
WSH.Echo "Hello world"
Set shell = CreateObject("WScript.shell")
'shell.Run "calc.exe"
'WScript.Quit

'Native VBS (not WSH):
MsgBox "hello world (from vb)"

cmd = "calc.exe"
WScript.Echo cmd
shell.Run cmd

'NOTE: `StdIn.ReadLine` only works if you run `cscript THISFILE.vbs`. Won't work from `wscript` interpreter.
WScript.StdOut.WriteLine "Press ENTER to continue..."
WScript.StdIn.ReadLine 'Pause before closing
WScript.StdOut.WriteLine "done"
