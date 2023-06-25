import os
import time
from threading import Thread
import ast
import sys

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
run = True
playMsg = True
cpuInt = int(psutil.cpu_percent())
textParseIterator = 0
version = " Version 1.2.5"
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
globalConf = [] 
hideSong = False #in conf
hideMiddle = False #in conf
hideOutside = False #in conf
showPaused = True #in conf
songDisplay = ' Listening to: 🎵{title} by {artist}🎵' #in conf
songName = ''
showOnChange = False #in conf
songChangeTicks = 1 #in conf
tickCount = 2
minimizeOnStart = False
keybind_run = 'p'
keybind_afk = 'end'
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
if os.path.isfile('please-do-not-delete.txt'):
  with open('please-do-not-delete.txt', 'r', encoding="utf-8") as f:
    try:
      fixed_list = ast.literal_eval(f.read())
      if len(fixed_list) == 26:
        topTextToggle = fixed_list[0]
        topTimeToggle = fixed_list[1]
        topSongToggle = fixed_list[2]
        topCPUToggle = fixed_list[3]
        topRAMToggle = fixed_list[4]
        topNoneToggle = fixed_list[5]
        bottomTextToggle = fixed_list[6]
        bottomTimeToggle = fixed_list[7]
        bottomSongToggle = fixed_list[8]
        bottomCPUToggle = fixed_list[9]
        bottomRAMToggle = fixed_list[10]
        bottomNoneToggle = fixed_list[11]
        message_delay = fixed_list[12]
        messageString = fixed_list[13]
        FileToRead = fixed_list[14]
        scrollText = fixed_list[15]
        hideSong = fixed_list[16]
        hideMiddle = fixed_list[17]
        hideOutside = fixed_list[18]
        showPaused = fixed_list[19]
        songDisplay = fixed_list[20]
        showOnChange = fixed_list[21]
        songChangeTicks = fixed_list[22]
        minimizeOnStart = fixed_list[23]
        keybind_run = fixed_list[24]
        keybind_afk = fixed_list[25]
      globalConf = fixed_list
    except:
      globalConf = []
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
  layout_layout = [[sg.Column(
              [[sg.Text('Configure chatbox layout', background_color='darkseagreen', font=('Arial', 12, 'bold'))],
              [sg.Column([
                  [sg.Checkbox('Text file read - defined in the behavior tab\n(This will disable everything else)', default=False, key='scroll', enable_events= True, background_color='dark slate blue')]
              ], key='topConf', background_color='dark slate blue', size=(379, 50))],
              [sg.Column([
                  [sg.Text('Configure top half of chatbox:', font=('Arial', 10, 'bold'))],
                  [sg.Checkbox('Text - Defined in the behavior tab', default=False, key='topText', enable_events= True)],
                  [sg.Checkbox('Time', default=False, key='topTime', enable_events= True)],
                  [sg.Checkbox('Song - Uses Windows\' MediaManager to request song info \n Does NOT pull directly from spotify', default=False, key='topSong', enable_events= True)],
                  [sg.Checkbox('CPU', default=False, key='topCPU', enable_events= True)],
                  [sg.Checkbox('RAM', default=False, key='topRAM', enable_events= True)],
                  [sg.Checkbox('None (Uncheck to select others)', default=True, key='topNone', enable_events= True)]
              ], key='topConf')],
              [sg.Column([
                  [sg.Text('Configure bottom half of chatbox:', font=('Arial', 10, 'bold'), background_color='peru')],
                  [sg.Checkbox('Text - Defined in the behavior tab', default=False, key='bottomText', enable_events= True, background_color='peru')],
                  [sg.Checkbox('Time', default=False, key='bottomTime', enable_events= True, background_color='peru')],
                  [sg.Checkbox('Song - Uses Windows\' MediaManager to request song info \n Does NOT pull directly from spotify', default=False, key='bottomSong', enable_events= True, background_color='peru')],
                  [sg.Checkbox('CPU', default=False, key='bottomCPU', enable_events= True, background_color='peru')],
                  [sg.Checkbox('RAM', default=False, key='bottomRAM', enable_events= True, background_color='peru')],
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
              ], size=(379, 130))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='DarkSlateGray4')]]

  keybindings_layout = [[sg.Column(
              [[sg.Text('Keybindings Configuration', background_color='turquoise4', font=('Arial', 12, 'bold'))],
               [sg.Text('You must press Apply for new keybinds to take affect!', background_color='turquoise4')],
                [sg.Column([
                  [sg.Text('Toggle Run'), sg.Frame('',[[sg.Text('Unbound', key='keybind_run', background_color='DarkSlateGray4', pad=(10, 0))]],background_color='DarkSlateGray4'), sg.Button('Bind Key', key='run_binding')],
                  [sg.Text('Toggle Afk'), sg.Frame('',[[sg.Text('Unbound', key='keybind_afk', background_color='DarkSlateGray4', pad=(10, 0))]],background_color='DarkSlateGray4'), sg.Button('Bind Key', key='afk_binding')]
                ], expand_x=True, size=(379, 70))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='turquoise4')]]
  
  options_layout = [[sg.Column(
              [[sg.Text('Configure Program', background_color='SteelBlue4', font=('Arial', 12, 'bold'))],
                [sg.Column([
                  [sg.Checkbox('Minimize on startup', default=False, key='minimizeOnStart', enable_events= True)]
                ], size=(379, 35))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='SteelBlue4')]]
  
  preview_layout = [[sg.Column(
              [[sg.Text('Preview (Not Perfect)', background_color='DarkGreen', font=('Arial', 12, 'bold'))],
              [sg.Column([
                [sg.Text('', key = 'messagePreviewFill', font=('Arial', 12 ), auto_size_text=True, size=(21, 100), justification='center')]
              ], size=(379, 150))]
              ]
  
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color='DarkGreen')]]
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
                  sg.Tab('Options', options_layout, background_color='SteelBlue4')
              ]], 
              key='mainTabs', tab_location='lefttop', selected_title_color='white', selected_background_color='gray', expand_x=True, expand_y=True
          )
      ],
      [sg.Button('Apply'), sg.Button('Reset'), sg.Text(version), sg.Checkbox('Run?', default=True, key='runThing', enable_events= True, background_color='peru'), sg.Checkbox('AFK', default=False, key='afk', enable_events= True, background_color='#cb7cef')]]

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
    window['songDisplay'].update(value=' Listening to: 🎵{title} by {artist}🎵')
    window['showOnChange'].update(value=False)
    window['songChangeTicks'].update(value=2)
    window['hideOutside'].update(value=False)
    window['hideMiddle'].update(value=False)
    window['showPaused'].update(value=True)
    window['hideSong'].update(value=False)
    window['minimizeOnStart'].update(value=False)
    window['keybind_run'].update(value='p')
    window['keybind_afk'].update(value='end')
  def pullVars():
    global playMsg
    global msgOutput
    if os.path.isfile('please-do-not-delete.txt'):
      if len(globalConf) == 26:
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
      else:
        resetVars()
    while run:
      if run:
        try:
          window['messagePreviewFill'].update(value=msgOutput)
        except Exception as e:
          print(e)
      time.sleep(.1)
      window['runThing'].update(value=playMsg)
      window['afk'].update(value=afk)
      
  pullVarsThread = Thread(target=pullVars)
  pullVarsThread.start()
  if minimizeOnStart:
    window.minimize()  
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
      if values['bottomNone']:
          window['bottomText'].update(value=False)
          window['bottomTime'].update(value=False)
          window['bottomSong'].update(value=False)
          window['bottomCPU'].update(value=False)
          window['bottomRAM'].update(value=False)
      if (not event == "topNone") and (not values['topText'] and not values['topTime'] and not values['topSong'] and not values['topCPU'] and not values['topRAM']):
          window['topNone'].update(value=True)
      if (not event == "bottomNone") and (not values['bottomText'] and not values['bottomTime'] and not values['bottomSong'] and not values['bottomCPU'] and not values['bottomRAM']):
          window['bottomNone'].update(value=True)
      if (event == "topText" or event == "topTime" or event == "topSong" or  event == "topCPU" or event == "topRAM"):
          window['topNone'].update(value=False)
          if not values[event]:
              window[event].update(value=False)
              if (not values['topText'] and not values['topTime'] and not values['topSong'] and not values['topCPU'] and not values['topRAM']):
                  window["topNone"].update(value=True)
          else:
              window[event].update(value=True)
      if (event == "bottomText" or event == "bottomTime" or event == "bottomSong" or  event == "bottomCPU" or event == "bottomRAM"):
          window['bottomNone'].update(value=False)
          if not values[event]:
              window[event].update(value=False)
              if (not values['bottomText'] and not values['bottomTime'] and not values['bottomSong'] and not values['bottomCPU'] and not values['bottomRAM']):
                  window["bottomNone"].update(value=True)
          else:
              window[event].update(value=True)
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
          with open('please-do-not-delete.txt', 'w', encoding="utf-8") as f:
            try:
              f.write(str([topTextToggle, topTimeToggle, topSongToggle, topCPUToggle, topRAMToggle, topNoneToggle, bottomTextToggle, bottomTimeToggle, bottomSongToggle, bottomCPUToggle, bottomRAMToggle, bottomNoneToggle, message_delay, messageString, FileToRead, scrollText, hideSong, hideMiddle, hideOutside, showPaused, songDisplay, showOnChange, songChangeTicks, minimizeOnStart, keybind_run, keybind_afk]))
            except Exception as e:
              sg.popup('Error saving config to file:\n'+str(e))
      if event == 'Check For Updates':
        sg.popup('Coming Soon!')
      if event == 'Open Github Page':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools')
      if event == 'About':
        about_popop_layout =  [[sg.Text('OSC Chat Tools by', font=('Arial', 11, 'bold'), pad=(0, 20)), sg.Text('Lioncat6', font=('Arial', 12, 'bold'), text_color='lime')],[sg.Text('Modules Used:',font=('Arial', 11, 'bold'))], [sg.Text('- PySimpleGUI\n - argparse\n - datetimedatetime\n - pythonoscudp_client\n - keyboard\n - asyncio\n - psutil\n - webbrowser\n - winsdk.windows.media.control\n')], [sg.Text('Python Version: '+str(sys.version))], [sg.Button('Ok')]]
        about_window = sg.Window('About', about_popop_layout)
        event, values = about_window.read()
        about_window.close()
      if event == 'runThing':
        msgPlayToggle()
      if event == 'Open Config File':
        os.system("start "+ 'please-do-not-delete.txt')
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

  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=9000,
      help="The port the OSC server is listening on")
  args = parser.parse_args()                                                                                        

  client = udp_client.SimpleUDPClient(args.ip, args.port)


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
      current_media_info = asyncio.run(get_media_info())

      artist = current_media_info['artist']
      title = current_media_info['title']
      album_title = current_media_info['album_title']  
      if mediaIs('PLAYING') or (not showPaused):
        songInfo= songDisplay.format(artist=artist,title=title,album_title=album_title)
      else:
        songInfo=songDisplay.format(artist=artist,title=title,album_title=album_title)+" (paused)"
      letsGetThatTime =" "+str(current_hour)+":"+current_minute+dayThing
      cpu = " Cpu: "+ str(psutil.cpu_percent())+"%"
      ram = " Ram: "+str(int(psutil.virtual_memory()[2]))+"%"
      
      
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
              if not (hideSong and mediaIs('PAUSED')):
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
          if toSend != '':
            if not hideOutside:
              msgOutput = '╔═════════════╗'+toSend+' ╚═════════════╝'
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
              if not (hideSong and mediaIs('PAUSED')):
                toSendTop = toSendTop+songInfo
              else: 
                toSendTop = ''
          if topCPUToggle:
            toSendTop = toSendTop+cpu
          if topRAMToggle:
            toSendTop = toSendTop+ram
          if topTimeToggle:
            toSendTop = toSendTop+letsGetThatTime
          if topTextToggle :
            toSendTop = toSendTop + a
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
              if not (hideSong and mediaIs('PAUSED')):
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
          if not(toSendBottom == '' or toSendTop == ''):
            if not hideOutside and not hideMiddle:
              msgOutput = '╔═════════════╗'+toSendTop+" ╠═════════════╣"+toSendBottom+' ╚═════════════╝'
            elif hideOutside and not hideMiddle:
              msgOutput = toSendTop+" ╠═════════════╣"+toSendBottom+' '
            elif not hideOutside and hideMiddle:
              msgOutput = '╔═════════════╗'+toSendTop+" "+toSendBottom+' ╚═════════════╝'
            elif hideOutside and hideMiddle:
              msgOutput = toSendTop+" "+toSendBottom+' '
          elif toSendBottom == '' and toSendTop == '':
            msgOutput = ''
          elif toSendBottom == '' or toSendTop == '':
            if not hideOutside and not hideMiddle:
              msgOutput = '╔═════════════╗'+toSendTop+toSendBottom+' ╚═════════════╝'
            elif hideOutside and not hideMiddle:
              msgOutput = toSendTop+toSendBottom+' '
            elif not hideOutside and hideMiddle:
              msgOutput = '╔═════════════╗'+toSendTop+toSendBottom+' ╚═════════════╝'
            elif hideOutside and hideMiddle:
              msgOutput = toSendTop+toSendBottom+' '
      elif afk:
        msgOutput = '╔═════════════╗'+a+' ╚═════════════╝'
      else:
        msgOutput = a
      if playMsg:
        client.send_message("/chatbox/input", [ str(msgOutput), True, False])
        #print(str(msgOutput))
      for x in range(int(message_delay*10)):
        time.sleep(.1)
        if not playMsg:
          break

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
  if keyboard.is_pressed(keybind_afk):
    afkToggle()
    
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
while run:
  msgPlayCheck()
  afkCheck()
  time.sleep(.01)