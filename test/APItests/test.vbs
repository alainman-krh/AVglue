'Aliases: WScript, WSH, wsh
'- Running from wscript [filename.vbs] will run in windows (graphical) mode.
'- Running from cscript [filename.vbs] will run in a console.
WSH.Echo "Hello world"
Set shell = WSH.CreateObject("WScript.shell")
'shell.Run "calc.exe"
'WScript.Quit

'Native VBS (not WSH):
MsgBox "hello world (from vb)"
