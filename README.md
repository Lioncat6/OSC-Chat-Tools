# OSC Chat Tools 
An osc script I made for Vrchat. Now with UI!
- Feature Requests are encouraged. You need something added? Let me know

![Preview](https://github.com/Lioncat6/OSC-Chat-Tools/blob/c4eafce187b862930472bb577c7fd0d021af7eda/preview.png)

OCT Is a standalone program used for interacting with Vrchat's OSC to send chat messages to the chatbox as well as other data in some cases

# Having Issues? 
 - Read the [FAQ](https://github.com/Lioncat6/OSC-Chat-Tools/wiki/FAQ)
 - Message me on discord @lioncat6
 - Create an issue https://github.com/Lioncat6/OSC-Chat-Tools/issues

# Features
 - Split top/bottom layout with customizable dividers
 - Animated text
 - Current time
 - Song info using the Windows media manager
 - CPU Info
 - RAM Info
 - Heart rate info using Pulsoid (Get a token from the 'Tokens' section of the dashboard)
 - AFK message activated with a keyboard shortcut or using the OSC to watch for when the player activates AFK mode in game
 - Customizable keyboard shortcuts
 - OSC Port forwarding (So multiple programs can listen to the OSC!)
 - Customizable OSC Listen port/address
 - TONS of customizability


# Installation:
## Exe file
 - https://github.com/Lioncat6/OSC-Chat-Tools/releases/latest
 - Windows SmartScreen will complain due to it not being signed
 - Run it through https://www.virustotal.com/ if you would like. Might get some false positives due to the packaged Python file being compressed
## Build it yourself
(Not recommended cause things might be broken before release)
 - Install python [https://www.python.org/downloads/](https://www.python.org/downloads/)
 - Install all of the required Python modules (`pip install {module name}`):
   - PySimpleGUI
   - argparse
   - datetime
   - python-osc
   - keyboard
   - asyncio
   - psutil
   - winsdk
   - websocket-client
 - In a command prompt window in the folder the `osc-chat-tools.py` is located in:
 - `pip install PyInstaller`
 - `python -m PyInstaller -wF --icon=oscicon.ico --clean osc-chat-tools.py`
 - Or run the included `build.bat` file
 - The resulting exe will be located in the `dist` folder

## Open up `osc-chat-tools.exe` and the code will do the rest!

### Side note... the song functionality will show whatever the last thing you were listening to was... including any website or video you were watching... So be careful.

# Keyboard Shortcuts 
All keyboard shortcuts can be rebound
- **`P`** Toggle Chatbox
- **`end`** Toggle AFK

# TO GET A PULSOID TOKEN
 - First set up a pulsoid account and link a device: https://pulsoid.net/registration
    - Coming soon (whenever Pusloid looks at my request to create a third-party app): Pulsoid App link.
    - [HRtoVRChat_OSC pulsoid link](https://pulsoid.net/oauth2/authorize?response_type=token&client_id=8c48435f-a0c6-4512-9bf7-6768678b625c&redirect_uri=&scope=data:heart_rate:read&state=&response_mode=web_page)
    - https://pulsoid.net/ui/keys - If you have a BRO Subscription

# Guide- last updated for 1.1.0
### [https://youtu.be/an7PLpDf5kE](https://youtu.be/an7PLpDf5kE)


# Coming soon:
 - Modular plugins system to replace hardcoded objects
 - Make the program install instead of being standalone to enable mods and assets and to improve boot time
 - Switch to a different ui engine cause while PySimeGUI is great... its *too* simple
 - Heartrate data through stronmo (Cheaper alternative to Pulsoid)
 - Speech To Text (Almost Done!)
 - GPU Stats
 - Framerate
 - Ping
 - VR/Desktop Display
 - Other fun shit!
