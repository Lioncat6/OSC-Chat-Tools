import os
import time
from threading import Thread
import ast
import sys
import requests


if not os.path.isfile('please-do-not-delete.txt'):
  """os.system("pip install python-osc")
  os.system("pip install argparse")
  os.system("pip install datetime")
  os.system("pip install keyboard")
  os.system("pip install asyncio")
  os.system("pip install psutil")
  os.system("pip install PySimpleGUI")"""
  with open('please-do-not-delete.txt', 'w', encoding="utf-8") as f:
      f.write('[]')

import PySimpleGUI as sg
import argparse
from datetime import datetime
from pythonosc import udp_client
import keyboard
import asyncio
import psutil
import webbrowser
from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
import winsdk.windows.media.control as wmc
from websocket import create_connection # websocket-client
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


run = True
playMsg = True
cpuInt = int(psutil.cpu_percent())
textParseIterator = 0
version = "1.4.1"
message_delay = 1.5
msgOutput = ''
topTextToggle = False #in conf
topTimeToggle = False #in conf
topSongToggle = False #in conf
topCPUToggle = False #in conf
topRAMToggle = False #in conf
topNoneToggle = True #in conf

bottomTextToggle = False #in conf
bottomTimeToggle = False #in conf
bottomSongToggle = False #in conf
bottomCPUToggle = False #in conf
bottomRAMToggle = False #in conf
bottomNoneToggle = True #in conf
messageString = '' #in conf
afk = False
FileToRead = '' #in conf
scrollText = False #in conf
scrollTexTSpeed = 6
hideSong = False #in conf
hideMiddle = False #in conf
hideOutside = False #in conf
showPaused = True #in conf
songDisplay = ' 🎵{title} ᵇʸ {artist}🎵' #in conf
songName = ''
showOnChange = False #in conf
songChangeTicks = 1 #in conf
tickCount = 2 #in conf
minimizeOnStart = False #in conf
keybind_run = 'p' #in conf
keybind_afk = 'end' #in conf
topBar = '╔═════════════╗' #in conf
middleBar = '╠═════════════╣' #in conf
bottomBar = '╚═════════════╝' #in conf
topHRToggle = False #in conf
bottomHRToggle = False #in conf
pulsoidToken = '' #in conf
hrConnected = False
heartRate = 0
errorExit = False
windowAccess = None
avatarHR = False #in conf
blinkOverride = False #in conf
blinkSpeed  = .5 #in conf
useAfkKeybind = False #in conf
toggleBeat = True #in conf
updatePrompt = True #in conf
outOfDate = False

isAfk = False
isVR = False #Never used as the game never actually updates vrmode 
isMute = False
isInSeat = False
voiceVolume = 0
isUsingEarmuffs = False

confVersion = '' #in conf

def afk_handler(unused_address, args):
    global isAfk
    isAfk = args
    print('isAfk', isAfk)
    
def mute_handler(unused_address, args):
    global isMute
    isMute = args
    print('isMute',isMute)
    
def inSeat_handler(unused_address, args):
    global isInSeat
    isInSeat = args
    print('isInSeat',isInSeat)
    
def volume_handler(unused_address, args):
    global voiceVolume
    voiceVolume = args
    #print('voiceVolume',voiceVolume)
    
def usingEarmuffs_handler(unused_address, args):
    global isUsingEarmuffs
    isUsingEarmuffs = args
    print('isUsingEarmuffs', isUsingEarmuffs)
    
def vr_handler(unused_address, args):# The game never sends this value from what I've seen
    global isVR
    if args ==1:
        isVR == True
    else:
        isVR == False
    print('isVR', isVR)

def update_checker(a):
  global updatePrompt
  global outOfDate
  global windowAccess
  global version
  url = 'https://api.github.com/repos/Lioncat6/OSC-Chat-Tools/releases'
  response = requests.get(url)

  if response.ok:
        data = response.json()
        if int(data[0]["tag_name"].replace('v', '').replace('.', '').replace(' ', '').replace('Version', '').replace('version', '')) != int(version.replace('v', '').replace('.', '').replace(' ', '').replace('Version', '').replace('version', '')):
          print("A new version is available! "+ data[0]["tag_name"].replace('v', '').replace(' ', '').replace('Version', '').replace('version', '')+" > " + version.replace('v', '').replace(' ', '').replace('Version', '').replace('version', ''))
          if updatePrompt:
            def updatePromptWaitThread():
              while windowAccess == None:
                time.sleep(.1)
                pass
              windowAccess.write_event_value('updateAvailable', data[0]["tag_name"].replace('v', '').replace(' ', '').replace('Version', '').replace('version', ''))
            updatePromptWaitThreadHandler = Thread(target=updatePromptWaitThread)
            updatePromptWaitThreadHandler.start()
          outOfDate = True
          def waitThread():
            while windowAccess == None:
                time.sleep(.1)
                pass
            windowAccess.write_event_value('markOutOfDate', '')
          waitThreadHandler = Thread(target=waitThread)
          waitThreadHandler.start()
        else:
          if a:
            windowAccess.write_event_value('popup', "Program is up to date! Version "+version)
          print("Program is up to date! Version "+version)
        
  else:
      print('Update Error occurred:', response.status_code)
      

async def get_media_info():
    sessions = await MediaManager.request_async()
    # This source_app_user_model_id check and if statement is optional
    # Use it if you want to only get a certain player/program's media
    # (e.g. only chrome.exe's media not any other program's).

    # To get the ID, use a breakpoint() to run sessions.get_current_session()
    # while the media you want to get is playing.
    # Then set TARGET_ID to the string this call returns.

    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        
        info = await current_session.try_get_media_properties_async()

        # song_attr[0] != '_' ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

    # It could be possible to select a program from a list of current
    # available ones. I just haven't implemented this here for my use case.
    # See references for more information.
    raise Exception('TARGET_PROGRAM is not the current media session')
  
async def getMediaSession():
    sessions = await MediaManager.request_async()
    session = sessions.get_current_session()
    return session
def mediaIs(state):
    session = asyncio.run(getMediaSession())
    if session == None:
        return False
    return int(wmc.GlobalSystemMediaTransportControlsSessionPlaybackStatus[state]) == session.get_playback_info().playback_status
  
confDataDict = { #this dictionary will always exclude position 0 which is the config version!
  "1.4.1" : ['confVersion', 'topTextToggle', 'topTimeToggle', 'topSongToggle', 'topCPUToggle', 'topRAMToggle', 'topNoneToggle', 'bottomTextToggle', 'bottomTimeToggle', 'bottomSongToggle', 'bottomCPUToggle', 'bottomRAMToggle', 'bottomNoneToggle', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideMiddle', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'topHRToggle', 'bottomHRToggle', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt'] 
}

if os.path.isfile('please-do-not-delete.txt'):
  with open('please-do-not-delete.txt', 'r', encoding="utf-8") as f:
    try:
      fixed_list = ast.literal_eval(f.read())
      if type(fixed_list[0]) is str:
        confVersion = fixed_list[0]
        confLoaderIterator = 1
        for i, x in enumerate(confDataDict[fixed_list[0]]):
          globals()[x] = fixed_list[i]
          #print(f"{x} = {fixed_list[i]}")
        print("Successfully Loaded config file version "+fixed_list[0])
      else:
        print('Config file is Too Old! Not Updating Values...')
    except:
      print('Config File Load Error! Not Updating Values...')
def uiThread():
  global version
  global msgOutput
  global message_delay
  global topTextToggle
  global topTimeToggle
  global topSongToggle
  global topCPUToggle
  global topRAMToggle
  global topNoneToggle
  global bottomTextToggle
  global bottomTimeToggle
  global bottomSongToggle
  global bottomCPUToggle
  global bottomRAMToggle
  global bottomNoneToggle
  global messageString
  global playMsg
  global run
  global afk
  global FileToRead
  global scrollText
  global hideSong
  global hideMiddle
  global hideOutside
  global showPaused
  global songDisplay
  global songName
  global showOnChange
  global songChangeTicks
  global minimizeOnStart
  global keybind_run
  global keybind_afk
  global topBar
  global middleBar
  global bottomBar
  global topHRToggle
  global bottomHRToggle
  global pulsoidToken
  global errorExit
  global windowAccess
  global avatarHR
  global blinkOverride
  global blinkSpeed
  global useAfkKeybind
  global toggleBeat
  global updatePrompt
  global outOfDate
  global confVersion
  layout_layout = [[sg.Column(
              [[sg.Text('Configure chatbox layout', background_color='darkseagreen', font=('Arial', 12, 'bold'))],
              [sg.Column([
                  [sg.Checkbox('Text file read - defined in the behavior tab\n(This will disable everything else)', default=False, key='scroll', enable_events= True, background_color='dark slate blue')]
              ], key='topConf', background_color='dark slate blue', size=(379, 50))],
              [sg.Column([
                  [sg.Checkbox('Pass through heartrate avatar parameters\nwithout showing it in the chatbox', default=False, key='avatarHR', enable_events= True, background_color='SteelBlue4')]
              ], key='topConf', background_color='SteelBlue4', size=(379, 50))],
              [sg.Column([
                  [sg.Text('Configure top half of chatbox:', font=('Arial', 10, 'bold'))],
                  [sg.Checkbox('Text - Defined in the behavior tab', default=False, key='topText', enable_events= True)],
                  [sg.Checkbox('Time', default=False, key='topTime', enable_events= True)],
                  [sg.Checkbox('Song - Uses Windows\' MediaManager to request song info \n Does NOT pull directly from spotify', default=False, key='topSong', enable_events= True)],
                  [sg.Checkbox('CPU', default=False, key='topCPU', enable_events= True)],
                  [sg.Checkbox('RAM', default=False, key='topRAM', enable_events= True)],
                  [sg.Checkbox('Heart Rate (Configure in Behavior)', default=False, key='topHRToggle', enable_events= True)],
                  [sg.Checkbox('None (Uncheck to select others)', default=True, key='topNone', enable_events= True)]
              ], key='topConf')],
              [sg.Column([
                  [sg.Text('Configure bottom half of chatbox:', font=('Arial', 10, 'bold'), background_color='peru')],
                  [sg.Checkbox('Text - Defined in the behavior tab', default=False, key='bottomText', enable_events= True, background_color='peru')],
                  [sg.Checkbox('Time', default=False, key='bottomTime', enable_events= True, background_color='peru')],
                  [sg.Checkbox('Song - Uses Windows\' MediaManager to request song info \n Does NOT pull directly from spotify', default=False, key='bottomSong', enable_events= True, background_color='peru')],
                  [sg.Checkbox('CPU', default=False, key='bottomCPU', enable_events= True, background_color='peru')],
                  [sg.Checkbox('RAM', default=False, key='bottomRAM', enable_events= True, background_color='peru')],
                  [sg.Checkbox('Heart Rate (Configure in Behavior)', default=False, key='bottomHRToggle', enable_events= True, background_color='peru')],
                  [sg.Checkbox('None (Uncheck to select others)', default=True, key='bottomNone', enable_events= True, background_color='peru')]
              ], key='bottomConf', background_color='peru')]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='darkseagreen')]]

  behavior_layout =  [[sg.Column(
              [[sg.Text('Configure chatbox behavior', background_color='DarkSlateGray4', font=('Arial', 12, 'bold'))],
              [sg.Column([
                  [sg.Text('Text to display for the message. One frame per line\nTo send a blank frame, use an asterisk(*) by itself on a line.')],
                  [sg.Multiline(default_text='OSC Chat Tools\nBy Lioncat6',
                      size=(50, 10), key='messageInput')]
              ], size=(379, 220))],
              [sg.Column([
                  [sg.Text('File to use for the text file read functionality')],
                  [sg.Button('Open File'), sg.Text('', key='message_file_path_display')]
              ], size=(379, 70))],
              [sg.Column([
                  [sg.Text('Delay between frame updates, in seconds')],
                  [sg.Slider(range=(1.5, 10), default_value=1.5, resolution=0.1, orientation='horizontal', size=(40, 15), key="msgDelay")]
              ], size=(379, 70))],
              [sg.Column([
                  [sg.Text('Template to use for song display.\nVariables = {artist}, {title}, {album_title}')],
                  [sg.Input(key='songDisplay', size=(50, 1))]
              ], size=(379, 80))],
              [sg.Column([
                  [sg.Text('Top Divider:')],
                  [sg.Input(key='topBar', size=(50, 1))],
                  [sg.Text('Middle Divider:')],
                  [sg.Input(key='middleBar', size=(50, 1))],
                  [sg.Text('Bottom Divider:')],
                  [sg.Input(key='bottomBar', size=(50, 1))],
                ], size=(379, 160))],
              [sg.Column([
                  [sg.Text('Misc. Settings:')],
                  [sg.Checkbox('Show \"(paused)\" after song when song is paused', default=True, key='showPaused', enable_events= True)],
                  [sg.Checkbox('Hide song when music is paused', default=False, key='hideSong', enable_events= True)],
                  [sg.Checkbox('Remove middle divider (when applicable)', default=False, key='hideMiddle', enable_events= True)],
                  [sg.Checkbox('Remove outside dividers (when applicable)', default=False, key='hideOutside', enable_events= True)],
              ], size=(379, 150))],
              [sg.Column([
                  [sg.Text('Only Show on song change settings:')],
                  [sg.Checkbox('Only show music on song change', default=False, key='showOnChange', enable_events=True)],
                  [sg.Text('Amount of frames to wait before the song name disappears')],
                  [sg.Slider(range=(1, 5), default_value=2, resolution=1, orientation='horizontal', size=(40, 15), key="songChangeTicks")]
              ], size=(379, 130))],
              [sg.Column([
                  [sg.Text('Heartrate Settings:')],
                  [sg.Text('Pulsoid Token:')],
                  [sg.Input(key='pulsoidToken', size=(50, 1))],
                  [sg.Checkbox('Heart Rate Beat', default=True, key='toggleBeat', enable_events=True)],
                  [sg.Checkbox('Override Beat', default=False, key='blinkOverride', enable_events=True)],
                  [sg.Text('Blink Speed (If Overridden)')],
                  [sg.Slider(range=(0, 5), default_value=.5, resolution=.1, orientation='horizontal', size=(40, 15), key="blinkSpeed")]
              ], size=(379, 210))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='DarkSlateGray4')]]

  keybindings_layout = [[sg.Column(
              [[sg.Text('Keybindings Configuration', background_color='turquoise4', font=('Arial', 12, 'bold'))],
               [sg.Text('You must press Apply for new keybinds to take affect!', background_color='turquoise4')],
                [sg.Column([
                  [sg.Text('Toggle Run'), sg.Frame('',[[sg.Text('Unbound', key='keybind_run', background_color='DarkSlateGray4', pad=(10, 0))]],background_color='DarkSlateGray4'), sg.Button('Bind Key', key='run_binding')],
                  [sg.Text('Imagine That there is a checkbox here :)')],
                  [sg.Text('Toggle Afk'), sg.Frame('',[[sg.Text('Unbound', key='keybind_afk', background_color='DarkSlateGray4', pad=(10, 0))]],background_color='DarkSlateGray4'), sg.Button('Bind Key', key='afk_binding')],
                  [sg.Checkbox('Use keybind (Otherwise, uses osc to check afk status)', default=False, enable_events=True, key='useAfkKeybind')]
                ], expand_x=True, size=(379, 130))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='turquoise4')]]
  
  options_layout = [[sg.Column(
              [[sg.Text('Configure Program', background_color='SteelBlue4', font=('Arial', 12, 'bold'))],
                [sg.Column([
                  [sg.Checkbox('Minimize on startup', default=False, key='minimizeOnStart', enable_events= True)],
                  [sg.Checkbox('Show update prompt', default=True, key='updatePrompt', enable_events= True)]
                ], size=(379, 60))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='SteelBlue4')]]
  preview_layout = [[sg.Column(
              [[sg.Text('Preview (Not Perfect)', background_color='DarkGreen', font=('Arial', 12, 'bold'))],
              [sg.Column([
                [sg.Text('', key = 'messagePreviewFill', font=('Arial', 12 ), auto_size_text=True, size=(21, 100), justification='center')]
              ], size=(379, 150))]
              ]
  
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='DarkGreen')]]
  
  osc_layout = [[sg.Column(
              [[sg.Text('OSC Options - Coming Soon', background_color='turquoise4', font=('Arial', 12, 'bold'))]
              ]  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='turquoise4')]]
  
  menu_def = [['&File', ['A&pply', '&Reset', '---', 'Open Config File', '---','E&xit' ]],
          ['&Help', ['&About', '---', 'Submit Feedback', '---', 'Open &Github Page', '&Check For Updates']]]
  topMenuBar = sg.Menu(menu_def, key="menuBar")
  right_click_menu = ['&Right', ['You thought']]
  layout = [
      [[topMenuBar]],
      [   
          sg.TabGroup([[
                  sg.Tab('Layout', layout_layout, background_color='darkseagreen'),
                  sg.Tab('Behavior', behavior_layout, background_color='DarkSlateGray4'),
                  sg.Tab('Preview', preview_layout, background_color='DarkGreen'),
                  sg.Tab('Keybindings', keybindings_layout, background_color='turquoise4'),
                  sg.Tab('Options', options_layout, background_color='SteelBlue4'),
                  sg.Tab('OSC Options', osc_layout, background_color='turquoise4')
              ]], 
              key='mainTabs', tab_location='lefttop', selected_title_color='white', selected_background_color='gray', expand_x=True, expand_y=True, size=(440, 300)
          )
      ],
      [sg.Button('Apply'), sg.Button('Reset'), sg.Text(" Version "+str(version), key='versionText'), sg.Checkbox('Run?', default=True, key='runThing', enable_events= True, background_color='peru'), sg.Checkbox('AFK', default=False, key='afk', enable_events= True, background_color='#cb7cef')]]

  window = sg.Window('OSC Chat Tools', layout,
                  default_element_size=(12, 1), resizable=True, finalize= True, size=(540, 600), right_click_menu=right_click_menu)
  window.set_min_size((500, 350))
  
  def resetVars():
    window['bottomText'].update(value=False)
    window['bottomTime'].update(value=False)
    window['bottomSong'].update(value=False)
    window['bottomCPU'].update(value=False)
    window['bottomRAM'].update(value=False)
    window['topText'].update(value=False)
    window['topTime'].update(value=False)
    window['topSong'].update(value=False)
    window['topCPU'].update(value=False)
    window['topRAM'].update(value=False)
    window['topNone'].update(value=True)
    window['bottomNone'].update(value=True)
    window['messageInput'].update(value='OSC Chat Tools\nBy Lioncat6')
    window['msgDelay'].update(value=1.5)
    window['songDisplay'].update(value=' 🎵{title} ᵇʸ {artist}🎵')
    window['showOnChange'].update(value=False)
    window['songChangeTicks'].update(value=2)
    window['hideOutside'].update(value=False)
    window['hideMiddle'].update(value=False)
    window['showPaused'].update(value=True)
    window['hideSong'].update(value=False)
    window['minimizeOnStart'].update(value=False)
    window['keybind_run'].update(value='p')
    window['keybind_afk'].update(value='end')
    window['topBar'].update(value='╔═════════════╗')
    window['middleBar'].update(value='╠═════════════╣')
    window['bottomBar'].update(value='╚═════════════╝')
    window['topHRToggle'].update(value='False')
    window['bottomHRToggle'].update(value='False')
    window['pulsoidToken'].update(value='')
    window['avatarHR'].update(value=False)
    window['blinkOverride'].update(value=False)
    window['blinkSpeed'].update(value=.5)
    window['useAfkKeybind'].update(value=False)
    window['toggleBeat'].update(value=True)
    window['updatePrompt'].update(value=True)
  def pullVars():
    global playMsg
    global msgOutput
    if os.path.isfile('please-do-not-delete.txt'):
      window['topText'].update(value=topTextToggle)
      window['topTime'].update(value=topTimeToggle)
      window['topSong'].update(value=topSongToggle)
      window['topCPU'].update(value=topCPUToggle)
      window['topRAM'].update(value=topRAMToggle)
      window['topNone'].update(value=topNoneToggle)
      window['bottomText'].update(value=bottomTextToggle)
      window['bottomTime'].update(value=bottomTimeToggle)
      window['bottomSong'].update(value=bottomSongToggle)
      window['bottomCPU'].update(value=bottomCPUToggle)
      window['bottomRAM'].update(value=bottomRAMToggle)
      window['bottomNone'].update(value=bottomNoneToggle )
      window['msgDelay'].update(value=message_delay)
      window['messageInput'].update(value=messageString)
      window['message_file_path_display'].update(value=FileToRead)
      window['scroll'].update(value=scrollText)
      window['hideSong'].update(value=hideSong)
      window['hideMiddle'].update(value=hideMiddle)
      window['hideOutside'].update(value=hideOutside)
      window['showPaused'].update(value=showPaused)
      window['songDisplay'].update(value=songDisplay)
      window['showOnChange'].update(value=showOnChange)
      window['songChangeTicks'].update(value=songChangeTicks)
      window['minimizeOnStart'].update(value=minimizeOnStart)
      window['keybind_run'].update(value=keybind_run)
      window['keybind_afk'].update(value=keybind_afk)
      window['topBar'].update(value=topBar)
      window['middleBar'].update(value=middleBar)
      window['bottomBar'].update(value=bottomBar)
      window['topHRToggle'].update(value=topHRToggle)
      window['bottomHRToggle'].update(value=bottomHRToggle)
      window['pulsoidToken'].update(value=pulsoidToken)
      window['avatarHR'].update(value=avatarHR) 
      window['updatePrompt'].update(value=updatePrompt)
    while run:
      if run:
        try:
          window['messagePreviewFill'].update(value=msgOutput)
        except Exception as e:
          print(e)
        if run:
          time.sleep(.1)
        if run:
          window['runThing'].update(value=playMsg)
          window['afk'].update(value=afk)   
  pullVarsThread = Thread(target=pullVars)
  pullVarsThread.start()
  if minimizeOnStart:
    window.minimize()  
  windowAccess = window
  while True:
      event, values = window.read()
      #print(event, values)
      if event == sg.WIN_CLOSED or event == "Exit" or event == "You thought":
          break
      if values['topNone']:
          window['topText'].update(value=False)
          window['topTime'].update(value=False)
          window['topSong'].update(value=False)
          window['topCPU'].update(value=False)
          window['topRAM'].update(value=False)
          window['topHRToggle'].update(value=False)
      if values['bottomNone']:
          window['bottomText'].update(value=False)
          window['bottomTime'].update(value=False)
          window['bottomSong'].update(value=False)
          window['bottomCPU'].update(value=False)
          window['bottomRAM'].update(value=False)
          window['bottomHRToggle'].update(value=False)
      if (not event == "topNone") and (not values['topText'] and not values['topTime'] and not values['topSong'] and not values['topCPU'] and not values['topRAM'] and not values['topHRToggle']):
          window['topNone'].update(value=True)
      if (not event == "bottomNone") and (not values['bottomText'] and not values['bottomTime'] and not values['bottomSong'] and not values['bottomCPU'] and not values['bottomRAM'] and not values['bottomHRToggle']):
          window['bottomNone'].update(value=True)
      if (event == "topText" or event == "topTime" or event == "topSong" or  event == "topCPU" or event == "topRAM" or event == 'topHRToggle'):
          window['topNone'].update(value=False)
          if not values[event]:
              window[event].update(value=False)
              if (not values['topText'] and not values['topTime'] and not values['topSong'] and not values['topCPU'] and not values['topRAM'] and not values['topHRToggle']):
                  window["topNone"].update(value=True)
          else:
              window[event].update(value=True)
      if (event == "bottomText" or event == "bottomTime" or event == "bottomSong" or  event == "bottomCPU" or event == "bottomRAM" or event == 'bottomHRToggle'):
          window['bottomNone'].update(value=False)
          if not values[event]:
              window[event].update(value=False)
              if (not values['bottomText'] and not values['bottomTime'] and not values['bottomSong'] and not values['bottomCPU'] and not values['bottomRAM'] and not values['bottomHRToggle']):
                  window["bottomNone"].update(value=True)
          else:
              window[event].update(value=True)
      if event == 'topHRToggle' or event == 'bottomHRToggle':
        if window['pulsoidToken'].get() == '':
          window['bottomHRToggle'].update(value=False)
          window['topHRToggle'].update(value=False)
          sg.popup('Please enter a pulsoid token in the behavior tab!')
      if values['scroll']:
          if window['message_file_path_display'].get() == '':
            window['scroll'].update(value=False)
            sg.popup('Please select a file in the behavior tab before enabling this option!')
          else:
            window['bottomText'].update(value=False)
            window['bottomTime'].update(value=False)
            window['bottomSong'].update(value=False)
            window['bottomCPU'].update(value=False)
            window['bottomRAM'].update(value=False)
            window['topText'].update(value=False)
            window['topTime'].update(value=False)
            window['topSong'].update(value=False)
            window['topCPU'].update(value=False)
            window['topRAM'].update(value=False)
            window['topHRToggle'].update(value=False)
            window['bottomHRToggle'].update(value=False)
            window['topNone'].update(value=True)
            window['bottomNone'].update(value=True)
      if event == 'Reset':
          answer = sg.popup_yes_no("Are you sure?\nThis will erase all of your entered text and reset the configuration file!")
          if answer == "Yes":
            resetVars()
      if event == 'Open File':
          message_file_path = sg.popup_get_file('Select a File', title='Select a File')
          window['message_file_path_display'].update(value=message_file_path)
      if event == 'Apply':
          confVersion = version
          topTextToggle = values['topText']
          topTimeToggle = values['topTime']
          topSongToggle = values['topSong']
          topCPUToggle = values['topCPU']
          topRAMToggle = values['topRAM']
          topNoneToggle = values['topNone']
          bottomTextToggle = values['bottomText']
          bottomTimeToggle = values['bottomTime']
          bottomSongToggle = values['bottomSong']
          bottomCPUToggle = values['bottomCPU']
          bottomRAMToggle = values['bottomRAM']
          bottomNoneToggle = values['bottomNone']
          message_delay = values['msgDelay']
          messageString = values['messageInput']
          FileToRead = window['message_file_path_display'].get()
          scrollText = values['scroll']
          hideSong = values['hideSong']
          hideMiddle = values['hideMiddle']
          hideOutside = values['hideOutside']
          showPaused = values['showPaused']
          songDisplay = values['songDisplay']
          showOnChange = values['showOnChange']
          songChangeTicks = values['songChangeTicks']
          minimizeOnStart = values['minimizeOnStart']
          keybind_run = window['keybind_run'].get()
          keybind_afk = window['keybind_afk'].get()
          topBar = values['topBar']
          middleBar = values['middleBar']
          bottomBar = values['bottomBar']
          topHRToggle = values['topHRToggle']
          bottomHRToggle = values['bottomHRToggle']
          pulsoidToken = values['pulsoidToken']
          avatarHR = values['avatarHR']
          blinkOverride = values['blinkOverride']
          blinkSpeed = values['blinkSpeed']
          useAfkKeybind = values['useAfkKeybind']
          toggleBeat = values['toggleBeat']
          updatePrompt = values['updatePrompt']
          with open('please-do-not-delete.txt', 'w', encoding="utf-8") as f:
            try:
              f.write(str([confVersion, topTextToggle, topTimeToggle, topSongToggle, topCPUToggle, topRAMToggle, topNoneToggle, bottomTextToggle, bottomTimeToggle, bottomSongToggle, bottomCPUToggle, bottomRAMToggle, bottomNoneToggle, message_delay, messageString, FileToRead, scrollText, hideSong, hideMiddle, hideOutside, showPaused, songDisplay, showOnChange, songChangeTicks, minimizeOnStart, keybind_run, keybind_afk,topBar, middleBar, bottomBar, topHRToggle, bottomHRToggle, pulsoidToken, avatarHR, blinkOverride, blinkSpeed, useAfkKeybind, toggleBeat, updatePrompt]))
            except Exception as e:
              sg.popup('Error saving config to file:\n'+str(e))
          """print('Popup Open') #Popup Shit is broken 
          apply_popup_layout = [[sg.Text('Applied!')]]
          apply_popup_window = sg.Window('Applied!', apply_popup_layout, size=(300, 90), element_justification='center', no_titlebar=True, modal=False, finalize=True)
          apply_popup_window.bring_to_front()
          time.sleep(1)
          apply_popup_window.close()
          print('Popup Close')"""
          
      if event == 'Check For Updates':
        update_checker(True)
      if event == 'Open Github Page':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools')
      if event == 'About':
        about_popop_layout =  [[sg.Text('OSC Chat Tools by', font=('Arial', 11, 'bold'), pad=(0, 20)), sg.Text('Lioncat6', font=('Arial', 12, 'bold'), text_color='lime')],[sg.Text('Modules Used:',font=('Arial', 11, 'bold'))], [sg.Text('- PySimpleGUI\n - argparse\n - datetime\n - pythonosc (udp_client)\n - keyboard\n - asyncio\n - psutil\n - webbrowser\n - winsdk (windows.media.control)\n - websocket-client')], [sg.Text('Python Version: '+str(sys.version))], [sg.Button('Ok')]]
        about_window = sg.Window('About', about_popop_layout)
        event, values = about_window.read()
        about_window.close()
      if event == 'runThing':
        msgPlayToggle()
      if event == 'Open Config File':
        if os.path.isfile('please-do-not-delete.txt'):
          try:
            os.system("start "+ 'please-do-not-delete.txt')
          except Exception as e:
            sg.Popup('Error opening config file: '+e)
        else:
          sg.Popup('Error opening config file: File not found')
      if event == 'Submit Feedback':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/issues')
      if event == 'afk':
        afk = values['afk']
      if event == 'run_binding':
        run_binding_layout = [[sg.Text('Press any key to bind to \'Toggle Run\'')],[sg.Text('', key='preview_bind')],[sg.Button('Ok', disabled=True, key='Ok'), sg.Button('Cancel', disabled=True, key='Cancel')]]
        run_binding_window = sg.Window('Bind \'Toggle Run\'', run_binding_layout, size=(300, 90), element_justification='center', no_titlebar=True, modal=True)
        def checkPressThread():
          run_binding_window['preview_bind'].update(value=keyboard.read_key())
          run_binding_window['Ok'].update(disabled=False)
          run_binding_window['Cancel'].update(disabled=False)
        checkThread = Thread(target=checkPressThread)
        checkThread.start()
        while True:
          event, values = run_binding_window.read()
          if event == 'Cancel':
            break
          if event == 'Ok':
            window['keybind_run'].update(value=run_binding_window['preview_bind'].get())
            break
        run_binding_window.close()
      if event == 'afk_binding':
        run_binding_layout = [[sg.Text('Press any key to bind to \'Toggle Afk\'')],[sg.Text('', key='preview_bind')],[sg.Button('Ok', disabled=True, key='Ok'), sg.Button('Cancel', disabled=True, key='Cancel')]]
        run_binding_window = sg.Window('Bind \'Toggle Afk\'', run_binding_layout, size=(300, 90), element_justification='center', no_titlebar=True, modal=True)
        def checkPressThread():
          run_binding_window['preview_bind'].update(value=keyboard.read_key())
          run_binding_window['Ok'].update(disabled=False)
          run_binding_window['Cancel'].update(disabled=False)
        checkThread = Thread(target=checkPressThread)
        checkThread.start()
        while True:
          event, values = run_binding_window.read()
          if event == 'Cancel':
            break
          if event == 'Ok':
            window['keybind_afk'].update(value=run_binding_window['preview_bind'].get())
            break
        run_binding_window.close()
      if event == 'mediaManagerError':
        sg.popup_error('Media Manager Failure. Please restart your system.\n\nIf this problem persists, please report an issue on github: https://github.com/Lioncat6/OSC-Chat-Tools/issues.\nFull Error:\n'+str(values[event]), keep_on_top="True")
        break
      if event == 'pulsoidError':
        playMsg = False
        sg.popup('Pulsoid Error: Please double check your token in the behavior tab and then toggle run to try again.\n\nIf this problem persists, please report an issue on github: https://github.com/Lioncat6/OSC-Chat-Tools/issues')
      if event == 'updateAvailable':
        update_available_layout = [
              [sg.Column([
                [sg.Text('A new update is available!')],
                [sg.Text(values['updateAvailable']+" > " + version.replace('v', ''))],
                [sg.Text("\nYou can disable this popup in the options tab")]
              ], element_justification='center')],
              [sg.Button("Close"), sg.Button("Download")]]
        updateWindow = sg.Window('Update Available!', update_available_layout, finalize=True)
        while run:
          event, values = updateWindow.read()
          if event == sg.WIN_CLOSED or event == 'Close':
            updateWindow.close()
            break
          if event == 'Download':
            webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/releases/latest')
      if event == 'markOutOfDate':
        if not "Update" in window['versionText'].get():
          window['versionText'].update(value=window['versionText'].get()+" - New Update Available")
      if event == 'popup':
        sg.popup(values['popup'])
  window.close()
  playMsg = False
  run = False
def processMessage(a):
  returnList = []
  if messageString.count('\n')>0:
    posForLoop = 0
    for x in range(messageString.count('\n')):
      returnList.append(messageString[posForLoop:messageString.find('\n', posForLoop+1)].replace('\n', ''))
      posForLoop = messageString.find('\n', posForLoop+1)
    returnList.append(messageString[posForLoop:len(messageString)].replace('\n', ''))
  else:
    returnList.append(messageString)
  return returnList

if __name__ == "__main__":

  parser2 = argparse.ArgumentParser()
  parser2.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser2.add_argument("--port", type=int, default=9000,
      help="The port the OSC server is listening on")
  args2 = parser2.parse_args()                                                                                        

  client = udp_client.SimpleUDPClient(args2.ip, args2.port)
 
  """parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=9001, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = Dispatcher()
  dispatcher.map("/avatar/parameters/AFK", afk_handler)
  dispatcher.map("/avatar/parameters/VRMode", vr_handler) # The game never sends this value from what I've seen
  dispatcher.map("/avatar/parameters/MuteSelf", mute_handler)
  dispatcher.map("/avatar/parameters/InStation", inSeat_handler)
  dispatcher.map("/avatar/parameters/Voice", volume_handler)
  dispatcher.map("/avatar/parameters/Earmuffs", usingEarmuffs_handler)
  def oscListenServer():
      server = osc_server.ThreadingOSCUDPServer(
          (args.ip, args.port), dispatcher)
      print("Serving on {}".format(server.server_address))
      server.serve_forever()
  oscListenServerThread = Thread(target=oscListenServer)
  oscListenServerThread.start()"""
 
  def sendMsg(a):
    global cpuInt
    global msgOutput
    global message_delay
    global topTextToggle
    global topTimeToggle
    global topSongToggle
    global topCPUToggle
    global topRAMToggle
    global topNoneToggle
    global bottomTextToggle
    global bottomTimeToggle
    global bottomSongToggle
    global bottomCPUToggle
    global bottomRAMToggle
    global bottomNoneToggle
    global messageString
    global playMsg
    global run
    global songName
    global songDisplay
    global songChangeTicks
    global tickCount
    global topBar
    global middleBar
    global bottomBar
    global topHRToggle
    global bottomHRToggle
    global pulsoidToken
    global errorExit
    global avatarHR
    global blinkOverride
    global blinkSpeed
    global useAfkKeybind
    global toggleBeat
    if playMsg:
      #preassembles
      now = datetime.now()
      current_hour = now.strftime("%H")
      current_minute = now.strftime("%M")
      if int(current_hour) >= 12:
          current_hour = int(current_hour)-12
          dayThing = "PM"
      else:
          dayThing = "AM"
      if int(current_hour) == 0:
          current_hour = 12  
      try:
        current_media_info = asyncio.run(get_media_info())
        artist = current_media_info['artist']
        title = current_media_info['title']
        album_title = current_media_info['album_title'] 
        mediaPlaying = mediaIs('PLAYING')
      except Exception as e:
        artist = 'Can\'t get artist'
        title = 'Can\'t get title'
        album_title = 'Can\'t get album title'
        mediaPlaying = False
        if 'TARGET_PROGRAM' in str(e):
          pass
        else:
          if windowAccess != None:
            try:
                windowAccess.write_event_value('mediaManagerError', e)
            except:
              pass
      if mediaPlaying or (not showPaused):
        songInfo= songDisplay.format(artist=artist,title=title,album_title=album_title)
      else:
        songInfo=songDisplay.format(artist=artist,title=title,album_title=album_title)+" (paused)"
      letsGetThatTime =" "+str(current_hour)+":"+current_minute+dayThing
      cpu = " Cpu: "+ str(psutil.cpu_percent())+"%"
      ram = " Ram: "+str(int(psutil.virtual_memory()[2]))+"%"
      hrInfo = " 💓"+str(heartRate)
      #message Assembler:
      if not scrollText and not afk:
        if topNoneToggle or bottomNoneToggle:
          toSend = ''
          if topSongToggle or bottomSongToggle:
            if showOnChange:
              if tickCount != 0:
                toSend = toSend+songInfo
                songName = current_media_info['title']
                tickCount = tickCount -1
              if current_media_info['title'] != songName:
                toSend = toSend+songInfo
                songName = current_media_info['title']
                tickCount = songChangeTicks -1
            else:
              if not (hideSong and not mediaPlaying):
                toSend = toSend+songInfo
              else: 
                toSend = ''
          if topCPUToggle or bottomCPUToggle:
            toSend = toSend+cpu
          if topRAMToggle or bottomRAMToggle:
            toSend = toSend+ram
          if topTimeToggle or bottomTimeToggle:
            toSend = toSend+letsGetThatTime
          if topTextToggle or bottomTextToggle:
            toSend = toSend + a
          if topHRToggle or bottomHRToggle:
            toSend = toSend + hrInfo
          if toSend != '':
            if not hideOutside:
              msgOutput = topBar+toSend+" "+bottomBar
            else:
              msgOutput = toSend
          else:
            msgOutput = ''
        else:
          toSendTop = ''
          toSendBottom = ''
          if topSongToggle:
            if showOnChange:
              if tickCount != 0:
                toSendTop = toSendTop+songInfo
                songName = current_media_info['title']
                tickCount = tickCount -1
              if current_media_info['title'] != songName:
                toSendTop = toSendTop+songInfo
                songName = current_media_info['title']
                tickCount = songChangeTicks -1
            else:
              if not (hideSong and not mediaPlaying):
                toSendTop = toSendTop+songInfo
              else: 
                toSendTop = ''
          if topCPUToggle:
            toSendTop = toSendTop+cpu
          if topRAMToggle:
            toSendTop = toSendTop+ram
          if topTimeToggle:
            toSendTop = toSendTop+letsGetThatTime
          if topTextToggle:
            toSendTop = toSendTop + a
          if topHRToggle:
            toSendTop = toSendTop + hrInfo
          if bottomSongToggle:
            if showOnChange:
              if tickCount != 0:
                toSendBottom = toSendBottom+songInfo
                songName = current_media_info['title']
                tickCount = tickCount -1
              if current_media_info['title'] != songName:
                toSendBottom = toSendBottom+songInfo
                songName = current_media_info['title']
                tickCount = songChangeTicks -1
            else:
              if not (hideSong and not mediaPlaying):
                toSendBottom = toSendBottom+songInfo
              else: 
                toSendBottom = ''
          if bottomCPUToggle:
            toSendBottom = toSendBottom+cpu
          if bottomRAMToggle:
            toSendBottom = toSendBottom+ram
          if bottomTimeToggle:
            toSendBottom = toSendBottom+letsGetThatTime
          if bottomTextToggle :
            toSendBottom = toSendBottom + a
          if bottomHRToggle:
            toSendBottom = toSendBottom + hrInfo
          if not(toSendBottom == '' or toSendTop == ''):
            if not hideOutside and not hideMiddle:
              msgOutput = topBar+toSendTop+" "+middleBar+toSendBottom+" "+bottomBar
            elif hideOutside and not hideMiddle:
              msgOutput = toSendTop+" "+middleBar+toSendBottom+' '
            elif not hideOutside and hideMiddle:
              msgOutput = topBar+toSendTop+" "+toSendBottom+" "+bottomBar
            elif hideOutside and hideMiddle:
              msgOutput = toSendTop+" "+toSendBottom+' '
          elif toSendBottom == '' and toSendTop == '':
            msgOutput = ''
          elif toSendBottom == '' or toSendTop == '':
            if not hideOutside and not hideMiddle:
              msgOutput = topBar+toSendTop+toSendBottom+" "+bottomBar
            elif hideOutside and not hideMiddle:
              msgOutput = toSendTop+toSendBottom+' '
            elif not hideOutside and hideMiddle:
              msgOutput = topBar+toSendTop+toSendBottom+" "+bottomBar
            elif hideOutside and hideMiddle:
              msgOutput = toSendTop+toSendBottom+' '
      elif afk:
        msgOutput = topBar+a+" "+bottomBar
      else:
        msgOutput = a
      if playMsg:
        client.send_message("/chatbox/input", [ str(msgOutput), True, False])
        #print(str(msgOutput))
      for x in range(int(message_delay*10)):
        time.sleep(.1)
        if not playMsg or not run:
          break

def hrConnectionThread():
  while run:
    global hrConnected
    global heartRate
    global pulsoidToken
    global client
    global blinkOverride
    global blinkSpeed
    global useAfkKeybind
    global toggleBeat
    if (topHRToggle or bottomHRToggle or avatarHR) and (playMsg or avatarHR):
      if not hrConnected:
        try:
          ws = create_connection("wss://dev.pulsoid.net/api/v1/data/real_time?access_token="+pulsoidToken+"&response_mode=text_plain_only_heart_rate")
          ws.settimeout(1) # Set a timeout of 1 second so the thread stops 
          hrConnected = True
          def pulsoidListen():
              global heartRate
              while True:
                  try:
                    event = ws.recv()
                    heartRate = event
                    client.send_message("/avatar/parameters/isHRActive", True)
                    client.send_message("/avatar/parameters/isHRConnected", True)
                    client.send_message("/avatar/parameters/HR", int(event))
                  except:
                    pass
                  if not run or not hrConnected:
                      break

          pulsoidListenThread = Thread(target=pulsoidListen)
          pulsoidListenThread.start()
          def blinkHR():
            global heartRate
            global blinkOverride
            global blinkSpeed
            global toggleBeat
            while hrConnected and run and (playMsg or avatarHR):
              if toggleBeat:
                client.send_message("/avatar/parameters/isHRBeat", True)
                time.sleep(.1)
                client.send_message("/avatar/parameters/isHRBeat", False)
                if blinkOverride:
                  time.sleep(blinkSpeed)
                else:
                  if int(heartRate) <= 0:
                    heartRate = 1
                  if 60/int(heartRate) > 5:
                    time.sleep(1)
                  else:
                    time.sleep(60/int(heartRate))
          blinkHRThread = Thread(target=blinkHR)
          blinkHRThread.start()
          print('Pulsoid Connection Started...')
        except Exception as e:
          if windowAccess != None:
            if playMsg:
              windowAccess.write_event_value('pulsoidError', e)
    if ((not topHRToggle and not bottomHRToggle and not avatarHR) or not (playMsg or avatarHR)) and hrConnected:
      hrConnected = False
      print('Pulsoid Connection Stopped')
    time.sleep(.3)
hrConnectionThreadRun = Thread(target=hrConnectionThread)
hrConnectionThreadRun.start()

def runmsg():
  global textParseIterator
  global playMsg
  global afk
  global FileToRead
  global scrollText
  while playMsg:
    if not afk and not scrollText:
      for x in processMessage(messageString):
        if x == "*":
          sendMsg(" ㅤ")
        else:
          sendMsg(" "+x)
    elif afk:
      sendMsg('AFK')
      sendMsg('ㅤ')
    elif scrollText:
      fileToOpen = open(FileToRead, "r")
      fileText = fileToOpen.read()
      if textParseIterator + 144 < len(fileText):
        sendMsg(fileText[textParseIterator:textParseIterator+144])
        textParseIterator = textParseIterator +144
      else: 
        sendMsg(fileText[textParseIterator:textParseIterator+len(fileText)-textParseIterator])
        textParseIterator = 0
    else:
      sendMsg('')
    
  client.send_message("/chatbox/input", [ "", True, False])
    
def msgPlayCheck():
  if keyboard.is_pressed(keybind_run):
    msgPlayToggle()

def msgPlayToggle():
  global playMsg
  if playMsg:
      playMsg = False
      time.sleep(.5)
  else:
    playMsg = True  
    msgThread = Thread(target=runmsg)
    msgThread.start()
    """cpuThread = Thread(target=cpuCheck)
    cpuThread.start()"""
    time.sleep(.5) 
"""def cpuCheck():
  while playMsg:
    global cpuInt
    cpuInt = int(psutil.cpu_percent(2)*10)"""
    
def afkCheck():
  global isAfk
  global afk
  if useAfkKeybind:
    if keyboard.is_pressed(keybind_afk):
      afkToggle()
  elif isAfk:
    afk = True
  else:
    afk = False
    
def afkToggle():
  global afk
  afk = not afk
  time.sleep(.5) 

def restartMsg():
  global playMsg
  playMsg = False
  time.sleep(1.5)
  playMsg = True  
  msgThread = Thread(target=runmsg)
  msgThread.start()


"""cpuThread = Thread(target=cpuCheck)
cpuThread.start()"""
msgThread = Thread(target=runmsg)
msgThread.start()
mainUI = Thread(target=uiThread)
mainUI.start()
update_checker(False)
while run:
  msgPlayCheck()
  afkCheck()
  time.sleep(.01)