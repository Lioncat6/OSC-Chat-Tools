# OSC Chat Tools 
An osc script I made for Vrchat. Now with UI!
- Feature Requests are encouraged. You need something added? Let me know

![Preview](https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/preview.png)

OCT Is a standalone program used for interacting with Vrchat's OSC to send chat messages to the chatbox as well as other data in some cases

# Having Issues? 
 - Read the [FAQ](https://github.com/Lioncat6/OSC-Chat-Tools/wiki/FAQ)
 - Message me on discord @lioncat6
 - Create an issue https://github.com/Lioncat6/OSC-Chat-Tools/issues

# Features
 - Fully customizable layout with divider and newline toggles
 - Animated text
 - Current time
 - Song info using the Windows media manager and now the [Spotify](https://spotify.com/) API!
 - CPU Info
 - RAM Info
 - Heart rate info using [Pulsoid](https://pulsoid.net/) or [HypeRate](https://www.hyperate.io/) 
 - AFK message activated with a keyboard shortcut or using the OSC to watch for when the player activates AFK mode in-game
 - Customizable keyboard shortcuts
 - OSC Port forwarding (So multiple programs can listen to the OSC!)
 - Customizable OSC Listen port/address
 - TONS of customizability


# Installation:
## Exe file
 - https://github.com/Lioncat6/OSC-Chat-Tools/releases/latest
 - Windows SmartScreen will complain due to it not being signed

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
   - pyperclip
 - In a command prompt window in the folder the `osc-chat-tools.py` is located in:
 - `pip install PyInstaller`
 - `python -m PyInstaller -wF --icon=oscicon.ico --clean osc-chat-tools.py`
 - Or run the included `build.bat` file
 - The resulting exe will be located in the `dist` folder

### Side note... the windows now playing song functionality will show whatever the last thing you were listening to was... including any website or video you were watching... So be careful.

# Keyboard Shortcuts 
All keyboard shortcuts can be rebound
- **`P`** Toggle Chatbox
- **`end`** Toggle AFK

# To get a Pulsoid Token
 - First set up a Pulsoid account and link a device: https://pulsoid.net/registration
 - Next, grab a Pulsoid token using one of the two below methods:
    - [OCT Pulsoid App link](https://pulsoid.net/oauth2/authorize?response_type=token&client_id=8070496f-f886-4030-8340-96d1d68b25cb&redirect_uri=&scope=data:heart_rate:read&state=&response_mode=web_page)
    - https://pulsoid.net/ui/keys - If you have a BRO Subscription
 - Paste the copied token into the behavior tab under the `💓HR` section

# Guide - Last update 1.5.6
 - https://www.youtube.com/watch?v=8D23oUzb-0Q

# Coming soon:
 - Modular plugins system to replace hardcoded objects
 - Make the program install instead of being standalone to enable mods and assets and to improve boot time
 - Switch to a different ui, probably some sort of electron app rather than a python based one
 - Heartrate data through stronmo (Cheaper alternative to Pulsoid)
 - Speech To Text (Almost Done!)
 - GPU Stats
 - Framerate
 - Ping
 - VR/Desktop Display
 - Other fun shit!
