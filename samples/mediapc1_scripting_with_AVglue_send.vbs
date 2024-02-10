'samples\mediapc1_scripting_with_AVglue_send.vbs
Set shell = CreateObject("WScript.Shell")
Set FS = CreateObject("Scripting.FileSystemObject")
THIS_DIR = FS.GetParentFolderName(WScript.ScriptFullName)
WScript.Echo "Make sure listener (server) process is running"

'Sample script that uses applets\Windows\AVglue_send.vbs to send signals:
'(Mimicks what you can get by launching script with keyboard mapping programs)
scriptname = "AVglue_send.vbs"
cmdbase = THIS_DIR & "\..\applets\Windows\" & scriptname
'Some commands to send
sigarray = Array(_
	"VOLMUTE 0",_
	"a b c d",_
	"VOLBTN 5",_
	"IR 0xABCD",_
	"NOGOOD",_
	"VOLMUTE"_
)

For Each sig In sigarray
	shell.Run cmdbase & " " & sig
Next
WScript.Echo "Sample " & scriptname & " done."