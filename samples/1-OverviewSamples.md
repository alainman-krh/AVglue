## Overview of `AVglue/samples/`

# Media PC test
<!----------------------------------------------------------------------------->
The listener application must first be launched to recieve/act on incomming signals:
- Run `1-launch_listener.py` to start up listener application.

Next, you can trigger actions by sending signals. You can test this with the following:
- `mediapc1_test.py`: Direct communication from a python app.
- `mediapc1_scripting_with_AVglue_send.vbs`: Indirect communication by sending
  signals through applet `AVglue_send.vbs`. This is the simplest method for external
  programs to interact with an AVglue listener applications.