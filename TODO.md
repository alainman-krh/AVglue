# Signal/Action
- User input generates a `Signal`: -> Which then triggers execution of a Task.
- Tasks define a list of actions to be performed.
- One such action is to trigger a virtual signal (one not physically obtained from an external sensor/transducer)
- 

# Virtual signals
A typical use case for virtual signals is when signals from multiple physical origins (ex: IR remote button or keyboard button) are to be considered equivalent.
- The use of virtual signals are optional (to allow for simpler defintion files).
- By mapping multiple physical signals onto a common single virtual signal, the user ensures both trigger & execute the exact same task.