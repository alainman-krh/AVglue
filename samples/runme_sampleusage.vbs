'launchers\Windows\runme_sampleusage.vbs
Set shell = CreateObject("WScript.Shell")
Set FS = CreateObject("Scripting.FileSystemObject")
THIS_DIR = FS.GetParentFolderName(WScript.ScriptFullName)
WScript.Echo "Make sure listener (server) process is running"

'Sample script that uses launchers\Windows\AVglue_send.vbs to send signals:
'(Mimicks what you can get by launching script with keyboard mapping programs)
scriptname = "AVglue_send.vbs" 'Assume in path
sigarray = Array(_
	"VOLMUTE 0",_
	"a b c d",_
	"VOLBTN 5",_
	"IR 0xABCD",_
	"NOGOOD",_
	"VOLMUTE"_
)

cmdbase = THIS_DIR & "\..\launchers\Windows\" & scriptname
For Each sig In sigarray
	shell.Run cmdbase & " " & sig
Next
WScript.Echo "Sample " & scriptname & " done."