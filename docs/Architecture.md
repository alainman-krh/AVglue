## AVglue: Architecture

# WARN
<!----------------------------------------------------------------------------->
Still under heavy flux. Not certain how to break down the problem/solution.

# Signal/Trap/Action
<!----------------------------------------------------------------------------->
Any user or device-generated input detected by a computer or micro-controller can be used to trigger a either a `Signal` or `Action`.

- `Signal`s must be caught by a `Trap` in order to first perform an `Action`.
- The available set of `Trap`s change depending on the mode.
- A mode is defined as a stack of trap layers.

For example:
- We are in "Blu-Ray" mode, which makes use of the `MainAV|BluRay` layer stack.
- That means we first try to trap the signal using the `MainAV` layer (TV+A/V receiver controls).. and then by `BluRay` layer (BluRay controls)
- A `device play` signal is first sent to the `MainAV` layer... but is not caught - so then tries the `BluRay` layer - where it gets detected (trapped), and emits the `play` signal of the blu-ray player
- Traps are sought by going through a layer stack

# Signal/Action
<!----------------------------------------------------------------------------->
- User input generates a `Signal`: -> Which then performs an action.
- One such action is to trigger a virtual signal (one not physically obtained from an external sensor/transducer)
- There are many types of actions:
  - Action_SendKey, Action_TriggerVirtualSignal, Action_TriggerComSignal
  - Action_ExecuteShell
- With `Action_ExecuteSequence`: You can even build up an action as a sequence of other actions.

# Virtual signals
<!----------------------------------------------------------------------------->
A typical use case for virtual signals is when signals from multiple physical origins (ex: IR remote button or keyboard button) are to be considered equivalent.
- The use of virtual signals are optional (to allow for simpler defintion files).
- By mapping multiple physical signals onto a common single virtual signal, the user ensures both trigger & performs the exact same action.