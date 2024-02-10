## Overview of `AVglue/samples/`

# Using Samples
In order to use samples in this directory, please ensure:
- to add `[AVglue_PKGDIR]/libpython` to `PYTHONPATH`,
- to use a python environment (suggest: `venv`) that has all require packages
  (`pip install [PACKAGE NAMES]`)

# Media PC test: Direct/No listener
<!----------------------------------------------------------------------------->
`mediapc1_test.py` is a simple python application that interacts with the
"mediapc1" control environment. It automatically sends out test signals, and
reacts to them without launching a separate process.

# Media PC test: No listener
<!----------------------------------------------------------------------------->
The `mediapc1_listener.py` application must first be launched to recieve/act on
incomming signals:
- Run `1-launch_listener.py` to start up listener application in a separate window.

Next, you can trigger actions by sending signals. You can test this with the following:
- `mediapc1_scripting_with_AVglue_send.vbs`: Indirect communication by sending
  signals through applet `AVglue_send.vbs`. This is the simplest method for external
  programs to interact with an AVglue listener applications.