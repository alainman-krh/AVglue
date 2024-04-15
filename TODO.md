# TODO
Add info here

# Samples
- Numpad generates tones

# To avoid constructing objects:
Action_TriggerLocal will be part of a Messaging class so it doesn't have to be created/destroyed constantly

# Example: Macro Remote
- 3 Modes: YT (launch YT+80% vol), Music (Launch spotify+100%vol), Math (Launch calc + 20%vol), Python (Launch python + mute)

# TODO
- Send IR somehow
  - Daughterboard?
  - Direct RP2040
- USB into RP2040? Serial into RP2040?
  - Talk to macro keypad
  - Talk to IR module
- Documentation / Re-org
- Level shifting to 5V?? Does 3.3V have enough power?
- How to make your python code into a service that runs in the background?
- How to quit with CTRL-C or something?