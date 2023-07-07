# OSC Chat Tools 
An osc script I made for Vrchat. Now with UI!
- Feature Requests are encouraged. You need something added? Let me know

![Preview](https://github.com/Lioncat6/OSC-Chat-Tools/blob/27ad5f1e7960cc6454ade1e00cf0006b6d6f53f9/preview.png)

OCT Is a standalone Python script used for interacting with Vrchat's OSC
### Python is not required to be installed on your system

# Having Issues? 
 - Read the [FAQ](https://github.com/Lioncat6/OSC-Chat-Tools/wiki/FAQ)

# Installation:
## Exe file
 - https://github.com/Lioncat6/OSC-Chat-Tools/releases/latest
## Build it yourself (Not recommended cause things might be broken before release)
 - Install python [https://www.python.org/downloads/](https://www.python.org/downloads/)
 - Install all of the required Python modules (`pip install {module name}`):
   - PySimpleGUI
   - argparse
   - datetime
   - pythonosc
   - keyboard
   - asyncio
   - psutil
   - webbrowser
   - winsdk
   - websocket-client
 - In a command prompt window in the folder the `osc-chat-tools.py` is located in:
 - `pip install PyInstaller`
 - `python -m PyInstaller -wF osc-chat-tools.py`
 - The resulting exe will be located in the `dist` folder

## Open up `osc-chat-tools.exe` and the code will do the rest!

### Side note... the song functionality will show whatever the last thing you were listening to was... including a website or video you were watching. So be careful.

# Keyboard Shortcuts (PC ONLY)
- **`P`** Toggle Chatbox

# TO GET A PULSOID TOKEN
 - First set up a pulsoid account and link a device: https://pulsoid.net/registration
    - Coming soon (whenever Pusloid looks at my request to create a third-party app): Pulsoid App link. 
    - https://pulsoid.net/ui/keys - If you have a BRO Subscription

# Guide- last updated for 1.1.0
### [https://youtu.be/an7PLpDf5kE](https://youtu.be/an7PLpDf5kE)

# Features
 - Split top/bottom layout with customizable dividers
 - Animated text
 - Current time
 - Song info using the Windows media manager
 - CPU Info
 - RAM Info
 - Heart rate info using Pulsoid (Get a token from the 'Tokens' section of the dashboard)
 - AFK message activated with a keyboard shortcut
 - Customizable keyboard shortcuts
 - TONS of customizability

# Coming soon:
 - Heartrate data through stronmo (Cheaper alternative to Pulsoid)
 - Speech To Text (Almost Done!)
 - Overhaul of the top/bottom system to be replaced with a more modular one
 - GPU Stats
 - Framerate
 - Ping
 - VR/Desktop Display
 - Voice mute status
 - Other fun shit!
