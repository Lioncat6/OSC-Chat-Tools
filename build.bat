pip install FreeSimpleGUI
pip install argparse
pip install datetime
pip install python-osc
pip install keyboard
pip install asyncio
pip install psutil
pip install winsdk
pip install websocket-client
pip install PyInstaller
pip install pyperclip
pip install requests
pip install flask
pip install pynvml
pip install wmi
REM Linux AMD GPU support only (won't build on Windows):
REM pip install pyamdgpuinfo
python -m PyInstaller -wF --icon=oscicon.ico --clean osc-chat-tools.py
