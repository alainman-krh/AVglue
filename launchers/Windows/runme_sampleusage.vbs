'launchers\Windows\runme_sampleusage.vbs
Set shell = CreateObject("WScript.Shell")
cmdbase = "AVglue_send.vbs" 'Assume in path

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
