## Overview of `AVglue/samples/`

# Using Samples
<!----------------------------------------------------------------------------->
In order to use samples in this directory, please ensure:
- to add `[AVglue_PKGDIR]/libpython` to `PYTHONPATH`,
- to use a python environment (suggest: `venv`) that has all require packages
  (`pip install [PACKAGE NAMES]`)

# Stand-alone application examples
<!----------------------------------------------------------------------------->
The AVglue library can be used directly to create custom python programs or
scripts.

# Stand-alone script example: MediaPC1 test
<!----------------------------------------------------------------------------->
`mediapc1_test.py` is a simple python application that interacts with the
"mediapc1" control environment. It automatically sends out test signals, and
reacts to them without launching a separate process.

# Stand-alone GUI example: Volume control (MediaPC1)
<!----------------------------------------------------------------------------->
`gui\volume_applet.py` is a simple Python/TK GUI applet that control volume
for the components defined in `MediaPC1`.
system definitions

# AVglue-as-a-service examples
<!----------------------------------------------------------------------------->
AVglue can be launched as a TCP/IP server/listener application.

The client application must first request a connection to a RUNNING AVglue
application through the IP:socket address of its listener process.

Once connected, signals are sent to the AVglue application with messages of the
following format:
```
SIGNAME [OPTIONAL_DATA_INT64]\n
SIGNAME [OPTIONAL_DATA_INT64]\n
SIGNAME [OPTIONAL_DATA_INT64]\n
```
where `\n` refers to the new line character.

## Server/listener example: MediaPC1
<!----------------------------------------------------------------------------->
The `mediapc1_listener.py` application is an example of AVglue-as-a service.
The application must first be launched to recieve/act on incomming signals:
- Run `1-launch_listener.py` to start up listener application in a separate window.

Once the listener is running, other applications can trigger actions by sending
signals. The following are examples demonstrating how to send signals from a
client applications:
- `../applet/Windows/AVglue_send.vbs` applet: Send a single signal to the
  AVglue listener process running at a hard-coded IP:socket address.
- `mediapc1_scripting_with_AVglue_send.vbs`: Example of a .vbs script sending
  multiple signals by means of the `AVglue_send.vbs` applet. This way, scripts
  don't directly need to establish the TCP/IP connections on their end.
