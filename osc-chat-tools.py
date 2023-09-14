import os
import time
import threading
from threading import Thread, Lock
import ast
import requests
from collections import defaultdict
import ctypes

if not os.path.isfile('please-do-not-delete.txt'):
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
import socket
import pyperclip
from flask import Flask, request
from werkzeug.serving import make_server
import hashlib
import base64
#import GPUtil
run = True
playMsg = True
textParseIterator = 0
version = "1.5.5"
message_delay = 1.5
msgOutput = ''
topTextToggle = False #Deprecated, only in use for converting old save files
topTimeToggle = False #Deprecated, only in use for converting old save files
topSongToggle = False #Deprecated, only in use for converting old save files
topCPUToggle = False #Deprecated, only in use for converting old save files
topRAMToggle = False #Deprecated, only in use for converting old save files
topNoneToggle = True #Deprecated, only in use for converting old save files

bottomTextToggle = False #Deprecated, only in use for converting old save files
bottomTimeToggle = False #Deprecated, only in use for converting old save files
bottomSongToggle = False #Deprecated, only in use for converting old save files
bottomCPUToggle = False #Deprecated, only in use for converting old save files
bottomRAMToggle = False #Deprecated, only in use for converting old save files
bottomNoneToggle = True #Deprecated, only in use for converting old save files
messageString = '' #in conf
afk = False
FileToRead = '' #in conf
scrollText = False #in conf
scrollTexTSpeed = 6
hideSong = False #in conf
hideMiddle = False #Deprecated, only in use for converting old save files
hideOutside = True #in conf
showPaused = True #in conf
songDisplay = ' 🎵\'{title}\' ᵇʸ {artist}🎶' #in conf
songName = ''
showOnChange = False #in conf
songChangeTicks = 1 #in conf
tickCount = 2
minimizeOnStart = False #in conf
keybind_run = 'p' #in conf
keybind_afk = 'end' #in conf
topBar = '╔═════════════╗' #in conf
middleBar = '╠═════════════╣' #in conf
bottomBar = '╚═════════════╝' #in conf
topHRToggle = False #Deprecated, only in use for converting old save files
bottomHRToggle = False #Deprecated, only in use for converting old save files
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
confVersion = '' #in conf
oscListenAddress = '127.0.0.1' #in conf
oscListenPort = '9001' #in conf
oscSendAddress = '127.0.0.1' #in conf
oscSendPort = '9000' #in conf
oscForewordAddress = '127.0.0.1' #in conf
oscForewordPort = '9002' #in conf
oscListen = False #in conf
oscForeword = False #in conf

layoutStorage = ''

output = ''
logOutput = False  #in conf

layoutString = '' #in conf
verticalDivider = "〣" #in conf

cpuDisplay = 'ᴄᴘᴜ: {cpu_percent}%'#in conf
ramDisplay = 'ʀᴀᴍ: {ram_percent}%  ({ram_used}/{ram_total})'#in conf
gpuDisplay = 'ɢᴘᴜ: {gpu_percent}%'#in conf
hrDisplay = '💓 {hr}'#in conf
playTimeDisplay = '⏳{hours}:{remainder_minutes}'#in conf
mutedDisplay = 'Muted 🔇'#in conf
unmutedDisplay = '🔊'#in conf
 
darkMode = 'False' #in conf

sendBlank = True
suppressDuplicates = False
sendASAP = False

useMediaManager = True
useSpotifyApi = False
spotifySongDisplay =  '🎵\'{title}\' ᵇʸ {artist}🎶 『{song_progress} / {song_length}』'

spotifyAccessToken = ''
spotifyRefreshToken = ''

###########Program Variables (not in conf)######### 

useHR = False

playTime = 0

oscForewordPortMemory = ''
oscForewordAddressMemory = ''
runForewordServer = False
oscListenPortMemory = ''
oscListenAddressMemory = ''
isListenServerRunning = False
listenServer = None
useForewordMemory = False

isAfk = False
isVR = False #Never used as the game never actually updates vrmode 
isMute = False
isInSeat = False
voiceVolume = 0
isUsingEarmuffs = False

vrcPID = None

playTimeDat = time.mktime(time.localtime(psutil.Process(vrcPID).create_time()))

lastSent = ''
sentTime = 0
sendSkipped = False

spotifyAuthCode = None #<- only needed for the spotify linking process (temp var)

spotify_client_id = '915e1de141b3408eb430d25d0d39b380'
spotify_redirect_uri = 'http://localhost:8000/callback'
spotifyLinkStatus = 'Unlinked'
cancelLink = False
spotifyPlayState = ''


def fatal_error(error = None):
  global run
  run = False
  """ctypes.windll.user32.MessageBoxW(None, u"OSC Chat Tools has encountered a fatal error.", u"OCT Fatal Error", 16)
  if error != None:
    result = ctypes.windll.user32.MessageBoxW(None, u"The program crashed with an error message. Would you like to copy it to your clipboard?", u"OCT Fatal Error", 3 + 64)
    if result == 6:
      pyperclip.copy(str(datetime.now())+" ["+threading.current_thread().name+"] "+str(error))
  result = ctypes.windll.user32.MessageBoxW(None, u"Open the github page to get support?", u"OCT Fatal Error", 3 + 64)
  if result == 6:
      webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/wiki/Fatal-Error-Crash')"""
  time.sleep(5)
  os._exit(0)

def afk_handler(unused_address, args):
    global isAfk
    isAfk = args
    #print('isAfk', isAfk)
    outputLog(f'isAfk {isAfk}')
    
def mute_handler(unused_address, args):
    global isMute
    isMute = args
    #print('isMute',isMute)
    outputLog(f'isMute {isMute}')
    
def inSeat_handler(unused_address, args):
    global isInSeat
    isInSeat = args
    #print('isInSeat',isInSeat)
    outputLog(f'isInSeat {isInSeat}')
    
def volume_handler(unused_address, args):
    global voiceVolume
    voiceVolume = args
    #print('voiceVolume',voiceVolume)
    #outputLog(f'voiceVolume {voiceVolume}')
def usingEarmuffs_handler(unused_address, args):
    global isUsingEarmuffs
    isUsingEarmuffs = args
    #print('isUsingEarmuffs', isUsingEarmuffs)
    outputLog(f'isUsingEarmuffs {isUsingEarmuffs}')
    
def vr_handler(unused_address, args):# The game never sends this value from what I've seen
    global isVR
    if args ==1:
        isVR == True
    else:
        isVR == False
    #print('isVR', isVR)
    outputLog(f'isVR {isVR}')

"""def thread_exists(name):
    for thread in threading.enumerate():
        if thread.name == name:
            return True
    return False"""
    
message_queue = []
queue_lock = Lock()
def outputLog(text):
    text = text.replace("\n", "\n    ")
    print(text)
    global threadName
    threadName = threading.current_thread().name
    def outputQueue():
        global threadName
        timestamp = datetime.now()
        with queue_lock:
            message_queue.append((timestamp, "["+threadName+"] "+text))
        while windowAccess is None:
            time.sleep(.01)
        with queue_lock:
            message_queue.sort(key=lambda x: x[0])
            for message in message_queue:
                windowAccess.write_event_value('outputSend', str(message[0]) + " " + message[1])
                try:
                  windowAccess['output'].Widget.see('end')
                except Exception as e:
                  fatal_error(e)
            message_queue.clear()
    outputQueueHandler = Thread(target=outputQueue)
    outputQueueHandler.start()
    
outputLog("OCT Starting...")

def update_checker(a):
  global updatePrompt
  global outOfDate
  global windowAccess
  global version
  url = 'https://api.github.com/repos/Lioncat6/OSC-Chat-Tools/releases'
  try:
    response = requests.get(url)
    if response.ok:
          data = response.json()
          if int(data[0]["tag_name"].replace('v', '').replace('.', '').replace(' ', '').replace('Version', '').replace('version', '')) != int(version.replace('v', '').replace('.', '').replace(' ', '').replace('Version', '').replace('version', '')):
            #print("A new version is available! "+ data[0]["tag_name"].replace('v', '').replace(' ', '').replace('Version', '').replace('version', '')+" > " + version.replace('v', '').replace(' ', '').replace('Version', '').replace('version', ''))
            outputLog("A new version is available! "+ data[0]["tag_name"].replace('v', '').replace(' ', '').replace('Version', '').replace('version', '')+" > " + version.replace('v', '').replace(' ', '').replace('Version', '').replace('version', ''))
            if updatePrompt:
              def updatePromptWaitThread():
                while windowAccess == None:
                  time.sleep(.1)
                  pass
                windowAccess.write_event_value('updateAvailable', data[0]["tag_name"].replace('v', '').replace(' ', '').replace('Version', '').replace('version', ''))
              updatePromptWaitThreadHandler = Thread(target=updatePromptWaitThread).start()
            outOfDate = True
            def waitThread():
              while windowAccess == None:
                  time.sleep(.1)
                  pass
              windowAccess.write_event_value('markOutOfDate', '')
            waitThreadHandler = Thread(target=waitThread).start()
          else:
            if a:
              windowAccess.write_event_value('popup', "Program is up to date! Version "+version)
            #print("Program is up to date! Version "+version)
            outputLog("Program is up to date! Version "+version)
          
    else:
        #print('Update Checking Error occurred:', response.status_code)
        outputLog('Update Checking Error occurred:', response.status_code)
  except Exception as e:
    outputLog('Update Checking Error occurred:', str(e))

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
  "1.4.1" : ['confVersion', 'topTextToggle', 'topTimeToggle', 'topSongToggle', 'topCPUToggle', 'topRAMToggle', 'topNoneToggle', 'bottomTextToggle', 'bottomTimeToggle', 'bottomSongToggle', 'bottomCPUToggle', 'bottomRAMToggle', 'bottomNoneToggle', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideMiddle', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'topHRToggle', 'bottomHRToggle', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt'],
  "1.4.20" : ['confVersion', 'topTextToggle', 'topTimeToggle', 'topSongToggle', 'topCPUToggle', 'topRAMToggle', 'topNoneToggle', 'bottomTextToggle', 'bottomTimeToggle', 'bottomSongToggle', 'bottomCPUToggle', 'bottomRAMToggle', 'bottomNoneToggle', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideMiddle', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'topHRToggle', 'bottomHRToggle', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput'],
  "1.5.0" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay'],
  "1.5.1" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode'],
  "1.5.2" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode'],
  "1.5.3" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP'],
  "1.5.4" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP'],
  "1.5.5" : ['confVersion', 'message_delay', 'messageString', 'FileToRead', 'scrollText', 'hideSong', 'hideOutside', 'showPaused', 'songDisplay', 'showOnChange', 'songChangeTicks', 'minimizeOnStart', 'keybind_run', 'keybind_afk','topBar', 'middleBar', 'bottomBar', 'pulsoidToken', 'avatarHR', 'blinkOverride', 'blinkSpeed', 'useAfkKeybind', 'toggleBeat', 'updatePrompt', 'oscListenAddress', 'oscListenPort', 'oscSendAddress', 'oscSendPort', 'oscForewordAddress', 'oscForeword', 'oscListen', 'oscForeword', 'logOutput', 'layoutString', 'verticalDivider','cpuDisplay', 'ramDisplay', 'gpuDisplay', 'hrDisplay', 'playTimeDisplay', 'mutedDisplay', 'unmutedDisplay', 'darkMode', 'sendBlank', 'suppressDuplicates', 'sendASAP', 'useMediaManager', 'useSpotifyApi', 'spotifySongDisplay', 'spotifyAccessToken', 'spotifyRefreshToken']
}

if os.path.isfile('please-do-not-delete.txt'):
  with open('please-do-not-delete.txt', 'r', encoding="utf-8") as f:
    try:
      fixed_list = ast.literal_eval(f.read())
      if type(fixed_list[0]) is str:
        confVersion = fixed_list[0]
        confLoaderIterator = 1
        if len(fixed_list) != len(confDataDict[confVersion]):
          raise Exception
        for i, x in enumerate(confDataDict[confVersion]):
          globals()[x] = fixed_list[i]
          #print(f"{x} = {fixed_list[i]}")
        #print("Successfully Loaded config file version "+fixed_list[0])
        outputLog("Successfully Loaded config file version "+fixed_list[0])
      else:
        #print('Config file is Too Old! Not Updating Values...')
        outputLog('Config file is Too Old! Not Updating Values...')
    except Exception as e:
      #print('Config File Load Error! Not Updating Values...')
      outputLog('Config File Load Error! Not Updating Values...')
  if confVersion == "1.4.1" or confVersion ==  "1.4.20":
    outputLog("Converting old layout system, please update your config by pressing apply!")
    if topTextToggle:
      layoutString = layoutString + '{text(0)}'
    if topTimeToggle:
      layoutString = layoutString + '{time(0)}'
    if topSongToggle:
      layoutString = layoutString + '{song(0)}'
    if topCPUToggle:
      layoutString = layoutString + '{cpu(0)}'
    if topRAMToggle:
      layoutString = layoutString + '{ram(0)}'
    if not hideMiddle and (topTextToggle or topTimeToggle or topSongToggle or topCPUToggle or topRAMToggle) and (bottomTextToggle or bottomTimeToggle or bottomSongToggle or bottomCPUToggle or bottomRAMToggle):
      layoutString = layoutString + '{div(0)}'
    if bottomTextToggle:
      layoutString = layoutString + '{text(0)}'
    if bottomTimeToggle:
      layoutString = layoutString + '{time(0)}'
    if bottomSongToggle:
      layoutString = layoutString + '{song(0)}'
    if bottomCPUToggle:
      layoutString = layoutString + '{cpu(0)}'
    if bottomRAMToggle:
      layoutString = layoutString + '{ram(0)}'
      
forewordServerLastUsed = oscForeword


layoutDisplayDict = {
    "playtime(" : "⌚Play Time",
    "text(" : "💬Text",
    "time(" : "🕒Time",
    "song(" : "🎵Song",
    "cpu(" : "⏱️CPU Usage",
    "ram(" : "🚦RAM Usage",
    "gpu(" : "⏳GPU Usage",
    "hr(" : "💓Heart Rate",
    "mute(" : "🔇Mute Status",
    "stt(" : "⌨Speech To Text",
    "div(" : "☵Divider"
                      }
def layoutPreviewBuilder(layout, window):
  def returnDisp(a):
    global layoutDisplayDict
    for x in layoutDisplayDict:
      if x in a:
        return layoutDisplayDict[x]

  try:
    layoutList = ast.literal_eval("["+layout.replace("{", "\"").replace("}", "\",")[:-1]+"]")
    layoutLen = len(layoutList)
    if layoutLen <=15:
      for x in range(layoutLen+1, 16):
        window['layout'+str(x)].update(visible=False)
      
      if layoutLen > 0:
        for x in range(1, layoutLen+1):
          window['layout'+str(x)].update(visible=True)
          window['text'+str(x)].update(value=returnDisp(layoutList[x-1]))
          if "3" in layoutList[x-1]:
            window['divider'+str(x)].update(value=True)
            window['newLine'+str(x)].update(value=True)
          elif "2" in layoutList[x-1]:
            window['newLine'+str(x)].update(value=True)
            window['divider'+str(x)].update(value=False)
          elif "1" in layoutList[x-1]: 
            window['divider'+str(x)].update(value=True)
            window['newLine'+str(x)].update(value=False)
          else:
            window['divider'+str(x)].update(value=False)
            window['newLine'+str(x)].update(value=False)
            
          
          

    else:
      for x in range(1, 16):
        window['layout'+str(x)].update(visible=False)
  except:
    for x in range(1, 16):
      window['layout'+str(x)].update(visible=False)
 
def refreshAccessToken(oldRefreshToken):
  global spotifyRefreshToken
  global spotifyAccessToken
  global spotify_client_id
  token_url = 'https://accounts.spotify.com/api/token'
  data = {
      'grant_type': 'refresh_token',
      'refresh_token': oldRefreshToken,
      'client_id': spotify_client_id
    }       
  response = requests.post(token_url, data=data)
  #print(response.json())
  spotifyRefreshToken = response.json().get('refresh_token')
  spotifyAccessToken =  response.json().get('access_token')    

def getSpotifyPlaystate():
  global spotifyRefreshToken
  global spotifyAccessToken
  
  def get_playstate(accessToken):
    global spotifyRefreshToken
    global spotifyAccessToken
    #print(spotifyAccessToken)
    #print(accessToken)
    headers = {
        'Authorization': 'Bearer ' + accessToken,
    }

    response = requests.get('https://api.spotify.com/v1/me/player', headers=headers)
    if response.status_code == 204:
      data = ''
    else:
      data = response.json()
    return data
  try:
      playState = get_playstate(spotifyAccessToken)
      if playState != '' and playState != None:
        if 'error' in str(playState):
          raise Exception('Error '+str(playState.get('error')))
  except Exception as e:
      outputLog("Regenerating spotify access token... "+str(e))
      accessToken = refreshAccessToken(spotifyRefreshToken)
      #windowAccess.write_event_value('Apply', '')  
      playState = get_playstate(accessToken) 
  if playState == None:
    playState = ''
  return playState
def loadSpotifyTokens():  
  global spotifyLinkStatus 
  if spotifyAccessToken != '' and spotifyAccessToken != None:
      outputLog("Loading spotify tokens...")
      def get_profile(accessToken):
          headers = {
              'Authorization': 'Bearer ' + accessToken,
          }
          response = requests.get('https://api.spotify.com/v1/me', headers=headers)
          data = response.json()
          if response.status_code != 200:
            raise Exception(response.json())
          return data
      try:
        outputLog("Trying old access token...")
        profile = get_profile(spotifyAccessToken)
      except Exception as e:
        outputLog("Attempting to regenerate outdated access token...\nReason: "+str(e))
        refreshAccessToken(spotifyRefreshToken)    
        profile = get_profile(spotifyAccessToken)
      linkedUserName = profile.get('display_name')  
      outputLog("Spotify linked to "+linkedUserName+" successfully!")
      spotifyLinkStatus = 'Linked to '+linkedUserName  
try:
  loadSpotifyTokens()
except Exception as e:
  spotifyLinkStatus = 'Error - Please Relink!'
  spotifyAccessToken = ''
  spotifyRefreshToken = ''
  outputLog("Spotify token load error! Please relink!\nFull Error: "+str(e))
def uiThread():
  global fontColor
  global bgColor
  global accentColor
  global scrollbarColor
  global buttonColor
  global scrollbarBackgroundColor
  global tabBackgroundColor
  global tabTextColor

  global version
  global msgOutput
  global message_delay
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
  global oscListenAddress
  global oscListenPort
  global oscSendAddress
  global oscSendPort
  global oscForewordAddress
  global oscForewordPort
  global oscListen
  global oscForeword
  global logOutput
  global layoutString
  global verticalDivider
  global layoutDisplayDict
  global cpuDisplay
  global ramDisplay
  global gpuDisplay
  global hrDisplay
  global playTimeDisplay
  global mutedDisplay
  global unmutedDisplay
  global darkMode
  global sendBlank
  global suppressDuplicates
  global sendASAP
  
  global useMediaManager
  global useSpotifyApi
  global spotifySongDisplay
  global spotifyAccessToken
  global spotifyRefreshToken
  global cancelLink
  global spotifyLinkStatus

  if darkMode:
    bgColor = '#333333'
    accentColor = '#4d4d4d'
    fontColor = 'grey85'
    buttonColor = accentColor
    scrollbarColor = accentColor
    scrollbarBackgroundColor = accentColor
    tabBackgroundColor = accentColor
    tabTextColor = fontColor
  else: 
    bgColor = '#64778d'
    accentColor = '#528b8b'
    fontColor = 'white'
    buttonColor = '#283b5b'
    scrollbarColor = '#283b5b'
    scrollbarBackgroundColor = '#a6b2be'
    tabBackgroundColor = 'white'
    tabTextColor = 'black'
  sg.set_options(sbar_frame_color=fontColor)
  sg.set_options(scrollbar_color=scrollbarColor)
  sg.set_options(button_color=(fontColor, buttonColor))
  sg.set_options(text_color=fontColor)
  sg.set_options(background_color=bgColor)
  sg.set_options(element_background_color=bgColor)
  sg.set_options(text_element_background_color=bgColor)
  sg.set_options(sbar_trough_color=scrollbarBackgroundColor)
  sg.set_options(border_width=0)
  sg.set_options(use_ttk_buttons=True)
  sg.set_options(input_elements_background_color=fontColor)
  
  
  new_layout_layout =  [[sg.Column(
              [[sg.Text('Configure chatbox layout', background_color=accentColor, font=('Arial', 12, 'bold')), sg.Checkbox('Text file read - defined in the behavior tab\n(This will disable everything else)', default=False, key='scroll', enable_events= True, background_color='dark slate blue')],
              [sg.Column([
                [sg.Text('Add Elements', font=('Arial', 12, 'bold'))],
                [sg.Text('Every Element is customizable from the Behavior Tab', font=('Arial', 10, 'bold'))],
                [sg.Text('*', text_color='cyan', font=('Arial', 12, 'bold'), pad=(0, 0)), sg.Text('= Requires OSC Listening To Function')],
                [sg.Text('💬Text', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('A configurable text object', ), sg.Push(), sg.Button('Add to Layout', key='addText')],
                [sg.Text('🕒Time', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display your current time', ), sg.Push(), sg.Button('Add to Layout', key='addTime')],
                [sg.Text('🎵Song', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Customizable song display', ), sg.Push(), sg.Button('Add to Layout', key='addSong')],
                [sg.Text('⏱️CPU', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display CPU Utilization %', ), sg.Push(), sg.Button('Add to Layout', key='addCPU')],
                [sg.Text('🚦RAM', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display RAM Usage %', ), sg.Push(), sg.Button('Add to Layout', key='addRAM')],
                [sg.Text('⏳GPU', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display GPU Utilization %', ), sg.Push(), sg.Button('Coming Soon', disabled=True, key='addGPU')],
                [sg.Text('💓HR', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display Heart Rate', ), sg.Push(), sg.Button('Add to Layout', key='addHR')],
                [sg.Text('🔇Mute', font=('Arial', 12, 'bold')), sg.Text('*', text_color='cyan', pad=(0, 0), font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Display Mic Mute Status', ), sg.Push(), sg.Button('Add to Layout', key='addMute')],
                [sg.Text('⌚Play Time', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Show Play Time', ), sg.Push(), sg.Button('Add to Layout',  key='addPlaytime')],
                [sg.Text('⌨️STT', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Speech recognition object', ), sg.Push(), sg.Button('Coming Soon', disabled=True, key='addSTT')],
                [sg.Text('☵Divider', font=('Arial', 12, 'bold')), sg.Push(), sg.Text('Horizontal Divider', ), sg.Push(), sg.Button('Add to Layout',  key='addDiv')],
                
                ],size=(350, 520), scrollable=True, vertical_scroll_only=True, element_justification='center'), sg.Column([
                  [sg.Text('Arrange Elements', font=('Arial', 12, 'bold'))],
                  [sg.Text('➥ = New Line  ┋ = Vertical Divider')],
                  [sg.Column([
                    [sg.Column([[sg.Button('❌', key='delete1'), sg.Button('⬆️', disabled=True, key='up1'), sg.Button('⬇️', key='down1'), sg.Text('---', key='text1',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', key="divider1", enable_events=True, font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine1")]], key='layout1', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete2'), sg.Button('⬆️', key='up2'), sg.Button('⬇️', key='down2'), sg.Text('---', key='text2',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider2",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine2")]], key='layout2', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete3'), sg.Button('⬆️', key='up3'), sg.Button('⬇️', key='down3'), sg.Text('---', key='text3',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider3",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine3")]], key='layout3', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete4'), sg.Button('⬆️', key='up4'), sg.Button('⬇️', key='down4'), sg.Text('---', key='text4',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider4",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine4")]], key='layout4', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete5'), sg.Button('⬆️', key='up5'), sg.Button('⬇️', key='down5'), sg.Text('---', key='text5',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider5",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine5")]], key='layout5', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete6'), sg.Button('⬆️', key='up6'), sg.Button('⬇️', key='down6'), sg.Text('---', key='text6',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider6",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine6")]], key='layout6', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete7'), sg.Button('⬆️', key='up7'), sg.Button('⬇️', key='down7'), sg.Text('---', key='text7',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider7",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine7")]], key='layout7', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete8'), sg.Button('⬆️', key='up8'), sg.Button('⬇️', key='down8'), sg.Text('---', key='text8',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider8",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine8")]], key='layout8', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete9'), sg.Button('⬆️', key='up9'), sg.Button('⬇️', key='down9'), sg.Text('---', key='text9',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider9",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine9")]], key='layout9', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete10'), sg.Button('⬆️', key='up10'), sg.Button('⬇️', key='down10'), sg.Text('---', key='text10',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider10",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine10")]], key='layout10', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete11'), sg.Button('⬆️', key='up11'), sg.Button('⬇️', key='down11'), sg.Text('---', key='text11',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider11",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine11")]], key='layout11', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete12'), sg.Button('⬆️', key='up12'), sg.Button('⬇️', key='down12'), sg.Text('---', key='text12',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider12",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine12")]], key='layout12', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete13'), sg.Button('⬆️', key='up13'), sg.Button('⬇️', key='down13'), sg.Text('---', key='text13',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider13",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine13")]], key='layout13', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete14'), sg.Button('⬆️', key='up14'), sg.Button('⬇️', key='down14'), sg.Text('---', key='text14',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider14",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine14")]], key='layout14', element_justification='left')],
                    [sg.Column([[sg.Button('❌', key='delete15'), sg.Button('⬆️', key='up15'), sg.Button('⬇️', key='down15'), sg.Text('---', key='text15',  font=('Arial', 10, 'bold')), sg.Checkbox('┋', enable_events=True, key="divider15",  font=('Arial', 10, 'bold')), sg.Checkbox('➥', enable_events=True, key="newLine15")]], key='layout15', element_justification='left')],
                    ], key="layout_editor", scrollable=True, vertical_scroll_only=True, element_justification='left', size=(335, 300))],
                  [sg.Text('Manual Edit', font=('Arial', 12, 'bold')), sg.Button('?', font=('Arial', 12, 'bold'), key="manualHelp")],
                  [sg.Text('Wrap object in { }. Spaces are respected.')],
                  [sg.Multiline('', key='layoutStorage', size=(45, 5), font=('Arial', 10, 'bold'))]
                  ], size=(360, 520), element_justification='center')]
              ]
  ,  expand_x=True, expand_y=True, background_color=accentColor, element_justification='left')]]


  
  misc_conf_layout = [
    [sg.Column([
                  [sg.Text('File to use for the text file read functionality')],
                  [sg.Button('Open File'), sg.Text('', key='message_file_path_display')]
              ], size=(379, 70))],
    [sg.Column([
                  [sg.Text('Delay between frame updates, in seconds')],
                  [sg.Text('If you are getting a \'Timed out for x seconds\' message,\ntry adjusting this')],
                  [sg.Slider(range=(1.5, 10), default_value=1.5, resolution=0.1, orientation='horizontal', size=(40, 15), key="msgDelay", trough_color=scrollbarBackgroundColor)]
      ], size=(379, 110))],
    [sg.Column([
      [sg.Text('Advanced Sending Options')],
      [sg.Checkbox('Clear the chatbox when toggled or on program close\nTurn off if you are getting issues with the chatbox blinking', key='sendBlank', default=True)],
      [sg.Checkbox('Skip sending duplicate messages', key='suppressDuplicates', default=False)],
      [sg.Checkbox('Send next message as soon as any data is updated\nOnly skips delay if previous message was skipped', key='sendASAP', default=False)]
    ], size=(379, 155))]
  ]
  
  text_conf_layout = [
    [sg.Column([
                  [sg.Text('Text to display for the message. One frame per line\nTo send a blank frame, use an asterisk(*) by itself on a line.\n\\n and \\v are respected.', justification='center')],
                  [sg.Multiline(default_text='OSC Chat Tools\nBy Lioncat6',
                      size=(50, 10), key='messageInput')]
    ], size=(379, 240))],
  ]
  time_conf_layout = [
  ]
  song_conf_layout = [
    [sg.Column([
                  [sg.Text("Select audio info source:")],
                  [sg.Checkbox("Windows Now Playing", key='useMediaManager', default=True, enable_events=True), sg.Checkbox("Spotify API", key='useSpotifyApi', default=False, enable_events=True)], #Its called the Now Playing Session Manager btw
                  ], size=(379, 80))],
    [sg.Column([
                  [sg.Text("Windows Now Playing settings:")],
                  [sg.Text('Template to use for song display.\nVariables: {artist}, {title}, {album_title}, {album_artist}')],
                  [sg.Input(key='songDisplay', size=(50, 1))]
    ], size=(379, 100))],
    [sg.Column([
                  [sg.Text("Spotify settings:")],
                  [sg.Text('Template to use for song display.\nVariables: {artist}, {title}, {album_title}, {album_artist}, \n{song_progress}, {song_length}, {volume}, {song_id}')],
                  [sg.Input(key='spotifySongDisplay', size=(50, 1))],
                  [sg.Button("Link Spotify 🔗", key="linkSpotify", button_color="#00a828", font="System"), sg.Text('Unlinked', key='spotifyLinkStatus', font="System", text_color='orange')],
    ], size=(379, 140))],
    [sg.Column([
                  [sg.Text('Music Settings:')],
                  [sg.Checkbox('Show \"⏸️\" after song when song is paused', default=True, key='showPaused', enable_events= True)],
                  [sg.Checkbox('Hide song when music is paused', default=False, key='hideSong', enable_events= True)],
                  [sg.HorizontalSeparator()],
                  [sg.Checkbox('Only show music on song change', default=False, key='showOnChange', enable_events=True)],
                  [sg.Text('Amount of frames to wait before the song name disappears')],
                  [sg.Slider(range=(1, 5), default_value=2, resolution=1, orientation='horizontal', size=(40, 15), key="songChangeTicks", trough_color=scrollbarBackgroundColor)]
              ], size=(379, 220))],
  ]
  cpu_conf_layout = [
    [sg.Column([
                  [sg.Text('Template to use for CPU display.\nVariables: {cpu_percent}')],
                  [sg.Input(key='cpuDisplay', size=(50, 1))]
              ], size=(379, 80))],
  ] 
  ram_conf_layout = [
    [sg.Column([
                  [sg.Text('Template to use for RAM display. Variables:\n{ram_percent}, {ram_available}, {ram_total}, {ram_used}')],
                  [sg.Input(key='ramDisplay', size=(50, 1))]
              ], size=(379, 80))],
  ]
  
  gpu_conf_layout = [
    [sg.Column([
                  [sg.Text('Template to use for GPU display.\nVariables: {gpu_percent}')],
                  [sg.Input(key='gpuDisplay', size=(50, 1))]
              ], size=(379, 80))],
  ]
  hr_conf_layout = [
    [sg.Column([
                  [sg.Text('Template to use for Heart Rate display.\nVariables: {hr}')],
                  [sg.Input(key='hrDisplay', size=(50, 1))]
              ], size=(379, 80))],
    [sg.Column([
                  [sg.Text('Heartrate Settings:')],
                  [sg.Checkbox('Pass through heartrate avatar parameters\neven when not running', default=False, key='avatarHR', enable_events= True)],
                  [sg.Text('Pulsoid Token:'), sg.Button('Get Token 💓', key='getPulsoidToken', font="System", button_color="#f92f60")],
                  [sg.Input(key='pulsoidToken', size=(50, 1))],
                  [sg.Checkbox('Heart Rate Beat', default=True, key='toggleBeat', enable_events=True)],
                  [sg.Checkbox('Override Beat', default=False, key='blinkOverride', enable_events=True)],
                  [sg.Text('Blink Speed (If Overridden)')],
                  [sg.Slider(range=(0, 5), default_value=.5, resolution=.01, orientation='horizontal', size=(40, 15), key="blinkSpeed", trough_color=scrollbarBackgroundColor)]
              ], size=(379, 260))]
  ]
  playTime_conf_layout = [
    [sg.Column([
                  [sg.Text('Template to use for Play Time display.\nVariables: {hours}, {remainder_minutes}, {minutes}')],
                  [sg.Input(key='playTimeDisplay', size=(50, 1))]
              ], size=(379, 80))],
  ]
  mute_conf_layout = [
    [sg.Column([
                  [sg.Text('Template to use for Mute Toggle display')],
                  [sg.Text('Muted:'), sg.Push(),  sg.Input(key='mutedDisplay', size=(30, 1))],
                  [sg.Text('Unmuted:'), sg.Push(), sg.Input(key='unmutedDisplay', size=(30, 1))]
              ], size=(379, 80))],
  ]
  divider_conf_layout = [
    [sg.Column([
                  [sg.Text('Divider Settings:')],
                  [sg.Text('Top Divider:')],
                  [sg.Input(key='topBar', size=(50, 1))],
                  [sg.Text('Middle Divider:')],
                  [sg.Input(key='middleBar', size=(50, 1))],
                  [sg.Text('Bottom Divider:')],
                  [sg.Input(key='bottomBar', size=(50, 1))],
                  [sg.Text('Vertical Divider:')],
                  [sg.Input(key='verticalDivider', size=(50, 1))],
                  [sg.Checkbox('Remove outside dividers', default=True, key='hideOutside', enable_events= True)],
                ], size=(379, 270))],
  ]
  new_behavior_layout = [
    [   
          sg.TabGroup([[
                  sg.Tab('❔Misc.', [[sg.Column(misc_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('💬Text', [[sg.Column(text_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('🕒Time', [[sg.Column(time_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('🎵Song', [[sg.Column(song_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('⏱️CPU', [[sg.Column(cpu_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('🚦RAM', [[sg.Column(ram_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('⏳GPU', [[sg.Column(gpu_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('💓HR', [[sg.Column(hr_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('🔇Mute', [[sg.Column(mute_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('⌚Play Time', [[sg.Column(playTime_conf_layout, background_color=accentColor)]], background_color=accentColor),
                  sg.Tab('⌨STT', [[sg.Text('Coming Soon')]], background_color=accentColor),
                  sg.Tab('☵Divider', [[sg.Column(divider_conf_layout, background_color=accentColor)]], background_color=accentColor),
              ]], 
              key='behaviorTabs', selected_title_color='white', selected_background_color='gray', expand_x=True, expand_y=True, size=(440, 300), font=('Arial', 11, 'normal'), tab_background_color=tabBackgroundColor, tab_border_width=0, title_color=tabTextColor, 
          )
      ],
  ]
  """behavior_layout =  [[sg.Column([
              [sg.Text('Configure chatbox behavior', background_color=accentColor, font=('Arial', 12, 'bold'))],
              [sg.Column(text_conf_layout, background_color=accentColor)],
              [sg.Column(time_conf_layout, background_color=accentColor)],
              [sg.Column(misc_conf_layout, background_color=accentColor)],
              [sg.Column(song_conf_layout, background_color=accentColor)],
              [sg.Column(cpu_conf_layout, background_color=accentColor)],
              [sg.Column(ram_conf_layout, background_color=accentColor)],
              [sg.Column(gpu_conf_layout, background_color=accentColor)],
              [sg.Column(hr_conf_layout, background_color=accentColor)],
              [sg.Column(playTime_conf_layout, background_color=accentColor)],
              [sg.Column(mute_conf_layout, background_color=accentColor)],
              [sg.Column(divider_conf_layout, background_color=accentColor)],             
              
              
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]"""

  keybindings_layout = [[sg.Column(
              [[sg.Text('Keybindings Configuration', background_color=accentColor, font=('Arial', 12, 'bold'))],
              [sg.Text('You must press Apply for new keybinds to take affect!', background_color=accentColor)],
                [sg.Column([
                  [sg.Text('Toggle Run'), sg.Frame('',[[sg.Text('Unbound', key='keybind_run', background_color=accentColor, pad=(10, 0))]],background_color=accentColor), sg.Button('Bind Key', key='run_binding')],
                  [sg.Checkbox('Use keybind', default=True, enable_events=True, key='useRunKeybind', disabled=True)],
                  [sg.Text('Toggle Afk'), sg.Frame('',[[sg.Text('Unbound', key='keybind_afk', background_color=accentColor, pad=(10, 0))]],background_color=accentColor), sg.Button('Bind Key', key='afk_binding')],
                  [sg.Checkbox('Use keybind (Otherwise, uses OSC to check afk status)', default=False, enable_events=True, key='useAfkKeybind')]
                ], expand_x=True, size=(379, 130))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]
  
  options_layout = [[sg.Column(
              [[sg.Text('Configure Program', background_color=accentColor, font=('Arial', 12, 'bold'))],
                [sg.Column([
                  [sg.Checkbox('Minimize on startup', default=False, key='minimizeOnStart', enable_events= True)],
                  [sg.Checkbox('Show update prompt', default=True, key='updatePrompt', enable_events= True)],
                  [sg.Checkbox('Dark Mode (applies on restart)', default=False, key='darkMode', enable_events=True)]
                ], size=(379, 90))]
              ]
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]
  preview_layout = [[sg.Column(
              [[sg.Text('Preview (Not Perfect)', background_color=accentColor, font=('Arial', 12, 'bold')),sg.Text('', key='sentCountdown')],
              [sg.Column([
                [sg.Text('', key = 'messagePreviewFill', font=('Arial', 12 ), auto_size_text=True, size=(23, 100), justification='center')]
              ], size=(379, 150))]
              ]
  
  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]
  
  osc_layout = [[sg.Column(
              [[sg.Text('OSC Options - Experimental\n(Turning on debug logging is recommended)', background_color=accentColor, font=('Arial', 12, 'bold'))],
              [sg.Column([
                  [sg.Text('OSC Listen Options')],
                  [sg.Checkbox('Use OSC Listen', key='oscListen')],
                  [sg.Text('Address: '), sg.Input('', size=(30, 1), key='oscListenAddress')],
                  [sg.Text('Port: '), sg.Input('', size=(30, 1), key='oscListenPort')]
                ], size=(379, 120))],
              [sg.Column([
                  [sg.Text('OSC Send Options')],
                  [sg.Text('Address: '), sg.Input('', size=(30, 1), key='oscSendAddress')],
                  [sg.Text('Port: '), sg.Input('', size=(30, 1), key='oscSendPort')]
                ], size=(379, 90))],
              [sg.Column([
                  [sg.Text('OSC Forwarding Options\nRepeats all listened data to another address for other programs')],
                  [sg.Checkbox('Use OSC Forwarding', key='oscForeword')],
                  [sg.Text('Address: '), sg.Input('', size=(30, 1), key='oscForewordAddress')],
                  [sg.Text('Port: '), sg.Input('', size=(30, 1), key='oscForewordPort')]
                ], size=(379, 150))]
              ]  , scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True, background_color=accentColor)]]
  
  output_layout =  [[sg.Column(
              [[sg.Text('Program Output', background_color=accentColor, font=('Arial', 12, 'bold')), sg.Checkbox('Log to file (OCT_debug_log.txt)', default=False, key='logOutput', background_color=accentColor)],
              [sg.Multiline('', disabled=True, key='output', size=(53, 30), background_color='DarkSlateGrey', text_color='white', expand_x=True, expand_y=True)]
              ] , expand_x=True, expand_y=True, background_color=accentColor)]]
  
  menu_def = [['&File', ['A&pply', '&Reset', '---', 'Open Config File', '---','E&xit', 'Re&start' ]],
          ['&Help', ['&About', '---', 'Submit Feedback', '---', 'Open &Github Page', '&Check For Updates', '&FAQ']]]
  topMenuBar = sg.Menu(menu_def, key="menuBar")
  right_click_menu = ['&Right', ['Copy', 'Paste']]
  layout = [
      [[topMenuBar]],
      [   
          sg.TabGroup([[
                  sg.Tab('🧩Layout', new_layout_layout, background_color=accentColor),
                  sg.Tab('🤖Behavior', new_behavior_layout, background_color=accentColor),
                  sg.Tab('📺Preview', preview_layout, background_color=accentColor),
                  sg.Tab('⌨Keybindings', keybindings_layout, background_color=accentColor),
                  sg.Tab('💻Options', options_layout, background_color=accentColor),
                  sg.Tab('📲OSC Options', osc_layout, background_color=accentColor),
                  sg.Tab('💾Output', output_layout, background_color=accentColor)
              ]], 
              key='mainTabs', tab_location='lefttop', selected_title_color='white', selected_background_color='gray', expand_x=True, expand_y=True, size=(440, 300), font=('Arial', 11, 'normal'), tab_background_color=tabBackgroundColor, tab_border_width=0, title_color=tabTextColor
          )
      ],
      [sg.Button('Apply', tooltip='Apply all changes to options'), sg.Button('Reset'), sg.Text(" Version "+str(version), key='versionText'), sg.Checkbox('Run?', default=True, key='runThing', enable_events= True, background_color='peru'), sg.Checkbox('AFK', default=False, key='afk', enable_events= True, background_color='#cb7cef')]]

  window = sg.Window('OSC Chat Tools', layout,
                  default_element_size=(12, 1), resizable=True, finalize= True, size=(900, 620), right_click_menu=right_click_menu)
  window.set_min_size((500, 350))
  def resetVars():
    window['messageInput'].update(value='OSC Chat Tools\nBy Lioncat6')
    window['msgDelay'].update(value=1.5)
    window['songDisplay'].update(value=' 🎵\'{title}\' ᵇʸ {artist}🎶')
    window['showOnChange'].update(value=False)
    window['songChangeTicks'].update(value=2)
    window['hideOutside'].update(value=True)
    window['showPaused'].update(value=True)
    window['hideSong'].update(value=False)
    window['minimizeOnStart'].update(value=False)
    window['keybind_run'].update(value='p')
    window['keybind_afk'].update(value='end')
    window['topBar'].update(value='╔═════════════╗')
    window['middleBar'].update(value='╠═════════════╣')
    window['bottomBar'].update(value='╚═════════════╝')
    window['pulsoidToken'].update(value='')
    window['avatarHR'].update(value=False)
    window['blinkOverride'].update(value=False)
    window['blinkSpeed'].update(value=.5)
    window['useAfkKeybind'].update(value=False)
    window['toggleBeat'].update(value=True)
    window['updatePrompt'].update(value=True)
    window['oscListenAddress'].update(value='127.0.0.1')
    window['oscListenPort'].update(value='9001')
    window['oscSendAddress'].update(value='127.0.0.1')
    window['oscSendPort'].update(value='9002')
    window['oscForewordAddress'].update(value='127.0.0.1')
    window['oscForewordPort'].update(value='9002')
    window['oscListen'].update(value=False)
    window['oscForeword'].update(value=False)
    window['logOutput'].update(value=False)
    window['layoutStorage'].update(value=False)
    window['verticalDivider'].update(value='〣')
    window['cpuDisplay'].update(value='ᴄᴘᴜ: {cpu_percent}%')
    window['ramDisplay'].update(value='ʀᴀᴍ: {ram_percent}%  ({ram_used}/{ram_total})')
    window['gpuDisplay'].update(value='ɢᴘᴜ: {gpu_percent}%')
    window['hrDisplay'].update(value='💓 {hr}')
    window['playTimeDisplay'].update(value='⏳{hours}:{remainder_minutes}')
    window['mutedDisplay'].update(value='Muted 🔇')
    window['unmutedDisplay'].update(value='🔊')
    window['darkMode'].update(value=False)
    window['sendBlank'].update(value=True)
    window['suppressDuplicates'].update(value=False)
    window['sendASAP'].update(value=False)
    window['useMediaManager'].update(value=True)
    window['useSpotifyApi'].update(value=False)
    window['spotifySongDisplay'].update(value='🎵\'{title}\' ᵇʸ {artist}🎶 『{song_progress} / {song_length}』')
    """window['spotifyAccessToken'].update(value='')
    window['spotifyRefreshToken'].update(value='')"""
  def updateUI():
    global bgColor
    global accentColor
    global fontColor
    global buttonColor
    global scrollbarColor 
    global scrollbarBackgroundColor
    global tabBackgroundColor
    global tabTextColor
    global playMsg
    global msgOutput
    global sentTime
    global sent
    global sendSkipped
    global message_delay
    global spotifyLinkStatus
    global spotifyAccessToken
    global spotifyRefreshToken
    if os.path.isfile('please-do-not-delete.txt'):
      try:
        window['msgDelay'].update(value=message_delay)
        window['messageInput'].update(value=messageString)
        window['message_file_path_display'].update(value=FileToRead)
        window['scroll'].update(value=scrollText)
        window['hideSong'].update(value=hideSong)
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
        window['pulsoidToken'].update(value=pulsoidToken)
        window['avatarHR'].update(value=avatarHR) 
        window['useAfkKeybind'].update(value=useAfkKeybind)
        window['updatePrompt'].update(value=updatePrompt)
        window['oscListenAddress'].update(value=oscListenAddress)
        window['oscListenPort'].update(value=oscListenPort)
        window['oscSendAddress'].update(value=oscSendAddress)
        window['oscSendPort'].update(value=oscSendPort)
        window['oscForewordAddress'].update(value=oscForewordAddress)
        window['oscForewordPort'].update(value=oscForewordPort)
        window['oscListen'].update(value=oscListen)
        window['oscForeword'].update(value=oscForeword)
        window['logOutput'].update(value=logOutput)
        window['layoutStorage'].update(value=layoutString)
        window['verticalDivider'].update(value=verticalDivider)
        window['cpuDisplay'].update(value=cpuDisplay)
        window['ramDisplay'].update(value=ramDisplay)
        window['gpuDisplay'].update(value=gpuDisplay)
        window['hrDisplay'].update(value=hrDisplay)
        window['playTimeDisplay'].update(value=playTimeDisplay)
        window['mutedDisplay'].update(value=mutedDisplay)
        window['unmutedDisplay'].update(value=unmutedDisplay)
        window['darkMode'].update(value=darkMode)
        window['sendBlank'].update(value=sendBlank)
        window['suppressDuplicates'].update(value=suppressDuplicates)
        window['sendASAP'].update(value=sendASAP)
        window['useMediaManager'].update(value=useMediaManager)
        window['useSpotifyApi'].update(value=useSpotifyApi)
        window['spotifySongDisplay'].update(value=spotifySongDisplay)
        """window['spotifyAccessToken'].update(value=spotifyAccessToken)
        window['spotifyRefreshToken'].update(value=spotifyRefreshToken)"""
        if spotifyLinkStatus != 'Unlinked':
          if 'Error' in spotifyLinkStatus:
            window['spotifyLinkStatus'].update(value=spotifyLinkStatus)
            window['spotifyLinkStatus'].update(text_color='red')
            window['linkSpotify'].update(text='Relink Spotify ⚠️', button_color= "red")
          else:
            window['linkSpotify'].update(text='Unlink Spotify 🔗', button_color= "#c68341")
            window['spotifyLinkStatus'].update(value=spotifyLinkStatus)
            window['spotifyLinkStatus'].update(text_color='green')
          window.write_event_value('Apply', '')    
      except Exception as e:
        print(str(e))
        pass
    while run:
      if run:
        try:
          window['messagePreviewFill'].update(value=msgOutput.replace("\v", "\n"))
          window['runThing'].update(value=playMsg)
          window['afk'].update(value=afk)   
          layoutPreviewBuilder(window['layoutStorage'].get(), window)
          if playMsg:
            sentTime = sentTime + 0.1
          if sendSkipped:
            window['sentCountdown'].update('Last sent: '+str(round(sentTime, 1)) +"/"+ "30" +" [Skipped Send]")
          else:
            window['sentCountdown'].update('Last sent: '+str(round(sentTime, 1)) +"/"+ str(message_delay))
        except Exception as e:
          fatal_error(e)
        if run:
          time.sleep(.1)
  updateUIThread = Thread(target=updateUI)
  updateUIThread.start()
  if minimizeOnStart:
    window.minimize()  
  windowAccess = window
  while True:
      event, values = window.read()
      #print(event, values)
      if event == sg.WIN_CLOSED or event == "Exit":
          break
      
      if event == 'Reset':
          answer = sg.popup_yes_no("Are you sure?\nThis will erase all of your entered text and reset the configuration file!")
          if answer == "Yes":
            resetVars()
      if event == 'Open File':
          message_file_path = sg.popup_get_file('Select a File', title='Select a File')
          window['message_file_path_display'].update(value=message_file_path)
      if event == 'Apply':
          confVersion = version
          message_delay = values['msgDelay']
          messageString = values['messageInput']
          FileToRead = window['message_file_path_display'].get()
          scrollText = values['scroll']
          hideSong = values['hideSong']
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
          pulsoidToken = values['pulsoidToken']
          avatarHR = values['avatarHR']
          blinkOverride = values['blinkOverride']
          blinkSpeed = values['blinkSpeed']
          useAfkKeybind = values['useAfkKeybind']
          toggleBeat = values['toggleBeat']
          updatePrompt = values['updatePrompt']
          oscListenAddress = values['oscListenAddress']
          oscListenPort = values['oscListenPort']
          oscSendAddress = values['oscSendAddress']
          oscSendPort = values['oscSendPort']
          oscForewordAddress = values['oscForewordAddress']
          oscForewordPort = values['oscForewordPort']
          oscListen = values['oscListen']
          oscForeword = values['oscForeword']
          logOutput = values['logOutput']
          layoutString = values['layoutStorage']
          verticalDivider = values['verticalDivider']
          cpuDisplay = values['cpuDisplay']
          ramDisplay = values['ramDisplay']
          gpuDisplay = values['gpuDisplay']
          hrDisplay = values['hrDisplay']
          playTimeDisplay = values['playTimeDisplay']
          mutedDisplay = values['mutedDisplay']
          unmutedDisplay = values['unmutedDisplay']
          darkMode = values['darkMode']
          sendBlank = values['sendBlank']
          suppressDuplicates = values['suppressDuplicates']
          sendASAP = values['sendASAP']
          useMediaManager = values['useMediaManager']
          useSpotifyApi = values['useSpotifyApi']
          spotifySongDisplay = values['spotifySongDisplay']
          """spotifyAccessToken = values['spotifyAccessToken']
          spotifyRefreshToken = values['spotifyRefreshToken']"""
          with open('please-do-not-delete.txt', 'w', encoding="utf-8") as f:
            try:
              f.write(str([confVersion, message_delay, messageString, FileToRead, scrollText, hideSong, hideOutside, showPaused, songDisplay, showOnChange, songChangeTicks, minimizeOnStart, keybind_run, keybind_afk,topBar, middleBar, bottomBar, pulsoidToken, avatarHR, blinkOverride, blinkSpeed, useAfkKeybind, toggleBeat, updatePrompt, oscListenAddress, oscListenPort, oscSendAddress, oscSendPort, oscForewordAddress, oscForeword, oscListen, oscForeword, logOutput, layoutString, verticalDivider,cpuDisplay, ramDisplay, gpuDisplay, hrDisplay, playTimeDisplay, mutedDisplay, unmutedDisplay, darkMode, sendBlank, suppressDuplicates, sendASAP,useMediaManager, useSpotifyApi, spotifySongDisplay, spotifyAccessToken, spotifyRefreshToken]))
            except Exception as e:
              sg.popup('Error saving config to file:\n'+str(e))
          
      if event == 'Check For Updates':
        update_checker(True)
      if event == 'Open Github Page':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools')
      if event == 'About':
        about_popop_layout =  [[sg.Text('OSC Chat Tools by', font=('Arial', 11, 'bold'), pad=(0, 20)), sg.Text('Lioncat6', font=('Arial', 12, 'bold'))],[sg.Text('Modules Used:',font=('Arial', 11, 'bold'))], [sg.Text('- PySimpleGUI\n - argparse\n - datetime\n - pythonosc (udp_client)\n - keyboard\n - asyncio\n - psutil\n - webbrowser\n - winsdk (windows.media.control)\n - websocket-client\n - pyperclip')], [sg.Button('Ok')]]
        about_window = sg.Window('About', about_popop_layout, keep_on_top=True)
        event, values = about_window.read()
        about_window.close()
      if event =='manualHelp':
        manual_help_layout =  [[sg.Column([
          [sg.Text('Manual Editing Guide', font=('Arial', 11, 'bold'))],
          [sg.Text('Warning: Manually editing the layout can cause errors if done incorrectly!', text_color='#e60000')],
          [sg.Text('Note: While putting plain text in the layout editor is supported,\nit will break the visual editor!', text_color="#6699ff", justification='center')],
          [sg.Text('Objects:', font=('Arial', 10, 'bold'))],
          [sg.Text(str(layoutDisplayDict).replace("\"", "").replace("(", "(data)").replace("\'", "").replace(",", "\n").replace("{", "").replace("}", "").replace(": ", " : "), font=('Arial', 11, 'bold'), justification='center')],
          [sg.Text('Data Guide (A data value is REQUIRED!):', font=('Arial', 10, 'bold'))],
          [sg.Text("0 : No Data\n1 : Vertical Line\n2 : New Line\n3 : Both Vertical Line and New Line", font=('Arial', 11, 'bold'), justification='center')],
        ],element_justification='center')]                      
        ,[sg.Text()], 
        [sg.Button('Ok')]]
        manual_help_window = sg.Window('About', manual_help_layout, keep_on_top=True)
        event, values = manual_help_window.read()
        manual_help_window.close()
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
      if event == 'scrollError':
        playMsg = False
        sg.popup('File Read Error: Please make sure you have a file selected to scroll though in the behavior tab, then toggle Run to try again!\nFull Error:\n' + str(values[event]), keep_on_top="True")
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
      if event == 'FAQ':
        webbrowser.open('https://github.com/Lioncat6/OSC-Chat-Tools/wiki/FAQ')
      if event == 'outputSend':
        current_text = values['output']
        if current_text == '':
          new_text = values[event]
        else:
          new_text = current_text + '\n' + values[event]
        window['output'].update(new_text)
        if logOutput:
          with open('OCT_debug_log.txt', 'a+', encoding="utf-8") as f:
            f.write("\n"+values[event])
      if event == 'listenError':
        outputLog(f'listenError {str(values[event])}')
        oscListen = False
        oscForeword = False
        window['oscListen'].update(value=False)
        window['oscForeword'].update(value=False)
        sg.popup('Please make sure no other program is listening to the osc and try re-enabling osc Listen/Foreword options.\n\nOSC Listen and Foreword have been disabled to this won\'t happen on startup')
        window.write_event_value('Apply', '')
      def layoutStorageAdd(a):
        if len(ast.literal_eval("["+window['layoutStorage'].get().replace("{", "\"").replace("}", "\",")[:-1]+"]")) < 15:
          window['layoutStorage'].update(value=values['layoutStorage']+" {"+a+"}")
        else:
          sg.popup("You have reached the limit of objects in the layout.\nYou can still add more in the manual edit section,\nhowever the UI will not reflect it")
      if event == 'addText':
        layoutStorageAdd("text(0)")
      if event == 'addTime':
        layoutStorageAdd("time(0)")
      if event == 'addSong':
        layoutStorageAdd("song(0)")
      if event == 'addCPU':
        layoutStorageAdd("cpu(0)")
      if event == 'addRAM':
        layoutStorageAdd("ram(0)")
      if event == 'addGPU':
        layoutStorageAdd("gpu(0)")
      if event == 'addHR':
        layoutStorageAdd("hr(0)")
      if event == 'addMute':
        layoutStorageAdd("mute(0)")
      if event == 'addSTT':
        layoutStorageAdd("stt(0)")
      if event == 'addDiv':
        layoutStorageAdd("div(0)")
      if event == 'addPlaytime':
        layoutStorageAdd("playtime(0)")
      def layoutMove(pos, up):
        layList = ast.literal_eval("["+window['layoutStorage'].get().replace("{", "\"").replace("}", "\",")[:-1]+"]")
        pos = pos-1
        if up:
          layList.insert(pos-1, layList.pop(pos))
        else:
          layList.insert(pos+1, layList.pop(pos))
        window['layoutStorage'].update(value=str(layList).replace("[", "").replace("\']", "}").replace("\"]", "}").replace("\",", "}").replace("\',", "}").replace("\"", "{").replace("\'", "{").replace("]", ""))
      def toggleValues(pos, data):
        layList = ast.literal_eval("["+window['layoutStorage'].get().replace("{", "\"").replace("}", "\",")[:-1]+"]")
        pos = pos-1
        editpos = layList[pos].find("(")+1
        if data == 1:
          layList[pos] = layList[pos][:editpos] + '1' + layList[pos][editpos+1:]
        elif data == 2:
          layList[pos] = layList[pos][:editpos] + '2' + layList[pos][editpos+1:]
        elif data == 3:
          layList[pos] = layList[pos][:editpos] + '3' + layList[pos][editpos+1:]
        else:
          layList[pos] = layList[pos][:editpos] + '0' + layList[pos][editpos+1:]
        if layList[pos][editpos+1:editpos+2] != ")":
          layList[pos] = layList[pos][:editpos+1] + ')' + layList[pos][editpos+1:]
        window['layoutStorage'].update(value=str(layList).replace("[", "").replace("\']", "}").replace("\"]", "}").replace("\",", "}").replace("\',", "}").replace("\"", "{").replace("\'", "{").replace("]", ""))
      for x in range(1, 16):
        if event == "delete"+str(x):
          listMod = ast.literal_eval("["+window['layoutStorage'].get().replace("{", "\"").replace("}", "\",")[:-1]+"]")
          del listMod[x-1]
          window['layoutStorage'].update(value=str(listMod).replace("[", "").replace("\']", "}").replace("\"]", "}").replace("\",", "}").replace("\',", "}").replace("\"", "{").replace("\'", "{").replace("]", ""))
        if event == "up"+str(x):
          layoutMove(x, True)
        if event == "down"+str(x):
          layoutMove(x, False)
        if event == "divider"+str(x) or event == "newLine"+str(x):
          if values['divider'+str(x)] and values['newLine'+str(x)]:
            toggleValues(x, 3)
          elif values['divider'+str(x)] and (not values['newLine'+str(x)]):
            toggleValues(x, 1)
          elif (not values['divider'+str(x)]) and values['newLine'+str(x)]:
            toggleValues(x, 2)
          else:
            toggleValues(x, 0)
      if event == 'Copy':
        keyboard.press_and_release('ctrl+c')
      if event == 'Paste':
        keyboard.press_and_release('ctrl+v')
      if event == 'getPulsoidToken':
        webbrowser.open('https://pulsoid.net/oauth2/authorize?response_type=token&client_id=8070496f-f886-4030-8340-96d1d68b25cb&redirect_uri=&scope=data:heart_rate:read&state=&response_mode=web_page')
      if event == 'useSpotifyApi':
        if spotifyAccessToken != '':
          window['useSpotifyApi'].update(value=True)
          window['useMediaManager'].update(value=False)
        else:
          sg.popup('Please link Spotify first!')
          window['useSpotifyApi'].update(value=False)
      if event == 'useMediaManager':
        window['useMediaManager'].update(value=True)
        window['useSpotifyApi'].update(value=False)
      if event == 'linkSpotify':
        if "Unlinked" in spotifyLinkStatus or "Error" in spotifyLinkStatus:
          linking_layout = [[sg.Text('')],[sg.Text('Linking Spotify...')],[sg.Button('Cancel')]]
          spotify_link_window = sg.Window('Linking Spotify...', linking_layout, size=(300, 90), element_justification='center', no_titlebar=True, modal=True)
          def spotifyLinkManager():
            global linking
            global linkedUserName
            linkedUserName = linkSpotify()
            linking = False
            spotify_link_window.write_event_value('done', 'done') 
          spotifyLinkThread = Thread(target=spotifyLinkManager).start()
          linking = True
          while linking:
            event, values = spotify_link_window.read()
            if event == 'Cancel':
              cancelLink = True
              linking = False
              break
            else:
              linking = False
              break
          spotify_link_window.close()
          window.write_event_value('Apply', '')
          window['spotifyLinkStatus'].update(value='Linked to '+linkedUserName)
          spotifyLinkStatus = 'Linked to '+linkedUserName
          window['spotifyLinkStatus'].update(text_color='green')
          window['linkSpotify'].update(text='Unlink Spotify 🔗', button_color= "#c68341")
        else:    
          spotifyAccessToken = ''
          spotifyRefreshToken = ''
          spotifyLinkStatus = 'Unlinked'
          window['useSpotifyApi'].update(value=False)
          window['useMediaManager'].update(value=True)
          useSpotifyApi = False
          useMediaManager = True
          window.write_event_value('Apply', '')
          window['spotifyLinkStatus'].update(value=spotifyLinkStatus)
          window['spotifyLinkStatus'].update(text_color='orange')
          window['linkSpotify'].update(text="Link Spotify 🔗", button_color="#00a828")
      if event == 'spotifyApiError':
        window['useSpotifyApi'].update(value=False)
        window['useMediaManager'].update(value=True)
        useSpotifyApi = False
        useMediaManager = True
        spotifyLinkStatus = 'Error - Please Relink!'
        spotifyAccessToken = ''
        spotifyRefreshToken = ''
        window.write_event_value('Apply', '')
        outputLog("Spotify api fetch error! Please relink!\nFull Error: "+str(values[event]))
        window['spotifyLinkStatus'].update(value=spotifyLinkStatus)
        window['spotifyLinkStatus'].update(text_color='red')
        window['linkSpotify'].update(text='Relink Spotify ⚠️', button_color= "red")
        sg.popup('Spotify api fetch error!\nAutomatically reverted to using Windows Now Playing\nPlease relink spotify in the behavior tab to continue...\nFull Error: '+str(values[event]))
  window.close()
  playMsg = False
  run = False
  try:
    listenServer.shutdown()
    listenServer.server_close()
  except:
    pass
  if logOutput:
    with open('OCT_debug_log.txt', 'a+', encoding="utf-8") as f:
        f.write("\n"+str(datetime.now())+" OCT Shutting down...")
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
  def oscClientDef():
    global client
    while run:
      parser2 = argparse.ArgumentParser()
      parser2.add_argument("--ip", default=oscSendAddress,
          help="The ip of the OSC server")
      parser2.add_argument("--port", type=int, default=oscSendPort,
          help="The port the OSC server is listening on")
      args2 = parser2.parse_args()                                                                                        

      client = udp_client.SimpleUDPClient(args2.ip, args2.port)
      time.sleep(.5)
  oscClientDefThread = Thread(target=oscClientDef)
  oscClientDefThread.start()

  dispatcher = Dispatcher()
  dispatcher.map("/avatar/parameters/AFK", afk_handler)
  dispatcher.map("/avatar/parameters/VRMode", vr_handler) # The game never sends this value from what I've seen
  dispatcher.map("/avatar/parameters/MuteSelf", mute_handler)
  dispatcher.map("/avatar/parameters/InStation", inSeat_handler)
  dispatcher.map("/avatar/parameters/Voice", volume_handler)
  dispatcher.map("/avatar/parameters/Earmuffs", usingEarmuffs_handler)
  
  def oscForwardingManager():
    global runForewordServer
    global oscListenAddressMemory
    global oscListenPortMemory
    global oscForewordAddressMemory
    global oscForewordPortMemory
    global oscForeword
    global oscListen
    global useForewordMemory
    global windowAccess
    time.sleep(.1)
    listen_socket = None
    forward_sockets = []
    while run:
        global runForewordServer
        global oscListenAddressMemory
        global oscListenPortMemory
        global oscForewordAddressMemory
        global oscForewordPortMemory
        global oscForeword
        global oscListen
        global useForewordMemory
        global windowAccess
        # Create a socket to listen for incoming data
        def create_sockets():
            nonlocal listen_socket
            global runForewordServer
            global oscListenAddressMemory
            global oscListenPortMemory
            global oscForewordAddressMemory
            global oscForewordPortMemory
            global oscForeword
            global oscListen
            global useForewordMemory
            global windowAccess
            try:
                listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                listen_socket.bind((oscListenAddress, int(oscListenPort)))
                listen_socket.settimeout(.5)
            except Exception as err:
                def WaitThread(err):
                    while windowAccess == None:
                        time.sleep(.1)
                        pass
                    windowAccess.write_event_value('listenError', str(err))
                updatePromptWaitThreadHandler = Thread(target=WaitThread, args=(err,)).start()

        # Set the IP addresses and port numbers to forward data to
        if oscForeword:
            forward_addresses = [
                ('127.0.0.1', 61394), #for the listen server
                (oscForewordAddress, int(oscForewordPort)),
            ]
        else:
            forward_addresses = [
                ('127.0.0.1', 61394) #for the listen server
            ]

        def dataSender():
            global runForewordServer
            global oscListenAddressMemory
            global oscListenPortMemory
            global oscForewordAddressMemory
            global oscForewordPortMemory
            global oscForeword
            global oscListen
            global useForewordMemory
            global windowAccess
            nonlocal forward_sockets
            runForewordServer = True
            #print('Starting Forwarding server on '+str(forward_addresses))
            create_sockets()
            outputLog('Starting Forwarding server on '+str(forward_addresses))
            oscListenAddressMemory = oscListenAddress
            oscListenPortMemory = oscListenPort
            oscForewordPortMemory = oscForewordPort
            oscForewordAddressMemory = oscForewordAddress
            useForewordMemory = oscForeword
            forward_sockets = [
              socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
              for _ in forward_addresses
            ]
            while run and runForewordServer:
                try:
                    data, addr = listen_socket.recvfrom(1024)

                    # Forward the data to each forward socket
                    for forward_socket, (ip, port) in zip(forward_sockets, forward_addresses):
                        forward_socket.sendto(data, (ip, port))
                except Exception as e:
                  time.sleep(.01)
                  pass
                

        if oscForeword:
            if not runForewordServer:
              if forewordServerLastUsed != oscForeword:
                outputLog("Foreword Server Toggled On... Waiting For Listen Server To Change Ports...")
                time.sleep(3)
              else:
                dataSenderThread = Thread(target=dataSender)
                dataSenderThread.start()
        time.sleep(.1)
        if oscListenAddressMemory != oscListenAddress or oscListenPortMemory != oscListenPort or oscForewordPortMemory != oscForewordPort or oscForewordAddressMemory != oscForewordAddress or useForewordMemory != oscForeword or useForewordMemory != oscForeword:
            if oscForeword:
                #print('Foreword/Listen Server Config Updated, Restarting Forwarding Server...\n')
                outputLog('Foreword/Listen Server Config Updated, Restarting Forwarding Server...\n')
                runForewordServer = False
                time.sleep(.5)
                if not runForewordServer:
                    dataSenderThread = Thread(target=dataSender)
                    dataSenderThread.start()
        if runForewordServer and not(oscForeword):
            if listen_socket is not None:
                listen_socket.close()
            for forward_socket in forward_sockets:
                forward_socket.close()
            runForewordServer = False
            #print('No OSC Foreword/Listening Options are selected, stopping Forwarding Server...')
            outputLog('No OSC Foreword/Listening Options are selected, stopping Forwarding Server...')
        time.sleep(.5)

    # Close all sockets on shutdown
    if listen_socket is not None:
        listen_socket.close()
    for forward_socket in forward_sockets:
        forward_socket.close()
  oscForwardingManagerThread = Thread(target=oscForwardingManager)
  oscForwardingManagerThread.start()
  def oscListenServerManager():
      global oscListenAddress
      global oscListenPort
      global oscListen
      global isListenServerRunning
      global forewordServerLastUsed
      while run:
          if oscListen:
              parser = argparse.ArgumentParser()
              if oscForeword:
                parser.add_argument("--ip",
                  default='127.0.0.1', help="The ip to listen on")
                parser.add_argument("--port",
                    type=int, default=61394, help="The port to listen on")
              else:
                parser.add_argument("--ip",
                  default=oscListenAddress, help="The ip to listen on")
                parser.add_argument("--port",
                    type=int, default=oscListenPort, help="The port to listen on")
              args = parser.parse_args()
              def listenServerThread():
                  global isListenServerRunning
                  global oscListenAddress
                  global oscListenPort
                  global listenServer
                  try:
                      if oscForeword:
                        location = "127.0.0.1:61394"
                      else:
                        location = f"{str(oscListenAddress)}:{str(oscListenPort)}"
                      outputLog('Attempting To Start Listen Server on '+location)
                      listenServer = osc_server.ThreadingOSCUDPServer(
                          (args.ip, args.port), dispatcher)
                      #print("Osc Listen Server Serving on {}".format(listenServer.server_address))
                      outputLog("Osc Listen Server Serving on {}".format(listenServer.server_address))
                      sockett = listenServer.socket
                      sockett.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                      
                      isListenServerRunning = True
                      
                      listenServer.serve_forever()           
                  except Exception as e:
                      #print('Osc Listen Server Failed to Start, Retying...'+str(e))
                      outputLog(f'Osc Listen Server Failed to Start, Retying...\nPlease make sure another program isn\'t using {location}\n'+str(e))
                      pass

              if not isListenServerRunning:
                  oscServerThread = Thread(target=listenServerThread)
                  oscServerThread.start()
          if not oscListen and isListenServerRunning:
            #print('No OSC Listen Options are Selected, Shutting Down OSC Listen Server...')
            outputLog('No OSC Listen Options are Selected, Shutting Down OSC Listen Server...')
            isListenServerRunning = False
            listenServer.shutdown()
            listenServer.server_close()
          if oscForeword != forewordServerLastUsed  and isListenServerRunning:
            outputLog('Foreword Server Toggled, Restarting Listen Server...')
            isListenServerRunning = False
            try:
              listenServer.shutdown()
              listenServer.server_close()
            except:
              pass
            forewordServerLastUsed = oscForeword
          time.sleep(.5)

  oscServerManagerThread = Thread(target=oscListenServerManager)
  oscServerManagerThread.start()

  
  
  def sendMsg(a):
    global msgOutput
    global message_delay
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
    global pulsoidToken
    global errorExit
    global avatarHR
    global blinkOverride
    global blinkSpeed
    global useAfkKeybind
    global toggleBeat
    global layoutString
    global verticalDivider
    global cpuDisplay
    global ramDisplay
    global gpuDisplay
    global hrDisplay
    global playTimeDisplay
    global mutedDisplay
    global unmutedDisplay
    global playTimeDat
    #stupid crap
    global letsGetThatTime
    global songInfo
    global cpuDat
    global ramDat
    global hrInfo
    global gpuDat
    global lastSent
    global sentTime
    global sendSkipped
    #end of stupid crap
    global timeVar
    timeVar = time.time()
    if playMsg:
      #message Assembler:
      if not scrollText and not afk:
        
        def msgGen(a):
          global verticalDivider
          global letsGetThatTime
          global songInfo
          global cpuDat
          global ramDat
          global hrInfo
          global msgOutput
          global hideSong
          global showPaused
          global useHR
          global gpuDat
          global timeVar
          global useSpotifyApi
          global useMediaManager
          useHR = False
          def checkData(msg, data):
            lf = "\v"
            if data == 1 or data == 3:
              msg = msg + " " + verticalDivider
            if data == 2 or data == 3:
              msg =  msg + lf
            return msg
          def time(data):
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
            letsGetThatTime =" "+str(current_hour)+":"+current_minute+dayThing
            return(checkData(letsGetThatTime, data))
          def text(data):
            return(checkData(a.replace("\\n", "\v").replace("\\v", "\v"), data))
          def song(data):
            global songInfo
            global useSpotifyApi
            global useMediaManager
            global spotifyLinkStatus
            global spotifyAccessToken
            global spotifyRefreshToken
            global spotifyPlayState
            if useMediaManager:
              try:
                current_media_info = asyncio.run(get_media_info())
                artist = current_media_info['artist']
                title = current_media_info['title']
                album_title = current_media_info['album_title'] 
                album_artist = current_media_info['album_artist'] 
                mediaPlaying = mediaIs('PLAYING')
              except Exception as e:
                artist = ''
                title = ''
                album_title = ''
                album_artist = ''
                mediaPlaying = False
                if 'TARGET_PROGRAM' in str(e):
                  logOutput('Can\'t get media info, please make sure an application is playing audio')
                  pass
                else:
                  if windowAccess != None:
                    try:
                        logOutput('mediaManagerError '+str(e))
                        windowAccess.write_event_value('mediaManagerError', e)
                    except:
                      pass
              if mediaPlaying or (not showPaused):
                songInfo = songDisplay.format_map(defaultdict(str, artist=artist,title=title,album_title=album_title, album_artist=album_artist))
              else:
                songInfo=songDisplay.format_map(defaultdict(str, artist=artist,title=title,album_title=album_title, album_artist=album_artist))+" ⏸️"
                
            else:
              def formatTime(seconds = 0):
                  minutes = int(seconds // 60)
                  remaining_seconds = int(seconds % 60)
                  return f"{minutes}:{remaining_seconds:02}"
              global spotifySongDisplay
              playState = spotifyPlayState
              if playState != None and playState != '': 
                artist = playState.get('item').get('artists')[0].get('name')
                title = playState.get('item').get('name')
                album_title = ''
                album_artist = ''
                song_progress = formatTime(playState.get('progress_ms')/1000)
                song_length = formatTime(playState.get('item').get('duration_ms')/1000)
                volume = str()
                song_id = playState.get('item').get('id')
                mediaPlaying = playState.get('is_playing')
              else:
                artist = ''
                title = ''
                album_title = ''
                album_artist = ''
                song_progress = formatTime(0)
                song_length = formatTime(0)
                volume = '0'
                song_id = 'N/A'
                mediaPlaying = False

              if mediaPlaying or (not showPaused):
                songInfo = spotifySongDisplay.format_map(defaultdict(str, artist=artist,title=title,album_title=album_title, album_artist=album_artist, song_progress=song_progress, song_length=song_length, volume=volume, song_id=song_id))
              else:
                songInfo=spotifySongDisplay.format_map(defaultdict(str, artist=artist,title=title,album_title=album_title, album_artist=album_artist, song_progress=song_progress, song_length=song_length, volume=volume, song_id=song_id))+" ⏸️"
            global showOnChange
            global songChangeTicks
            global tickCount
            #global songInfo
            global songName
            if hideSong and not mediaPlaying or title == '':
              return ''
            else:
              if showOnChange:
                if songInfo != songName:
                  tickCount = songChangeTicks
                  songName = songInfo
                if tickCount != 0:
                  tickCount = tickCount-1
                  return(checkData(songInfo, data))
                else:
                  return ''
              else:
                return(checkData(songInfo, data))
          def cpu(data):
            cpu_percent = str(psutil.cpu_percent())
            cpuDat = cpuDisplay.format_map(defaultdict(str, cpu_percent=cpu_percent))
            return (checkData(cpuDat, data))
          def ram(data):
            psutilVirtualMemory = psutil.virtual_memory()
            ram_percent = str(int(psutilVirtualMemory[2]))
            ram_used = str(round(int(psutilVirtualMemory[0])/1073741824-int(psutilVirtualMemory[1])/1073741824, 1))
            ram_available = str(round(int(psutilVirtualMemory[1])/1073741824, 1))
            ram_total = str(round(int(psutilVirtualMemory[0])/1073741824, 1))
            ramDat = ramDisplay.format_map(defaultdict(str, ram_percent=ram_percent, ram_available=ram_available, ram_total=ram_total, ram_used=ram_used))
            return (checkData(ramDat, data))
          def gpu(data):
            #gpu_percent = str(round((GPUtil.getGPUs()[0].load*100), 1))
            gpu_percent = "0"
            gpuDat = gpuDisplay.format_map(defaultdict(str, gpu_percent=gpu_percent))
            return (checkData(gpuDat, data))
          def hr(data):
            global useHR
            hr = str(heartRate)
            hrInfo = hrDisplay.format_map(defaultdict(str, hr=hr))
            useHR = True
            return (checkData(hrInfo, data))
          def mute(data):
            return (checkData("Coming Soon", data))
          def stt(data):
            return (checkData("Coming Soon", data))
          def div(data):
            return (checkData(middleBar, data))
          def mute(data):
            if isMute: 
              return (checkData(mutedDisplay, data))
            else:
              return (checkData(unmutedDisplay, data))
          def playtime(data):
            global timeVar
            try:
              minutes = int((timeVar-playTimeDat)/60)
              hours, remainder_minutes = divmod(minutes, 60)
              if vrcPID == None:
                minutes = 0
                hours = 0
                remainder_minutes = 0
            except Exception as e:
              minutes = 0
              hours = 0
              remainder_minutes = 0
            playDat = playTimeDisplay.format_map(defaultdict(str, hours="{:02d}".format(hours), remainder_minutes="{:02d}".format(remainder_minutes), minutes="{:02d}".format(minutes)))
            return(checkData(playDat, data))
          try:
            msgOutput = eval("f'"f'{layoutString}'"'")
          except Exception as e:
            msgOutput = "Layout Error!\v"+str(e)
          if msgOutput[-len(verticalDivider+" "):] == verticalDivider+" ":
            msgOutput = msgOutput[:-len(verticalDivider+" ")-1]
          if msgOutput[-len(middleBar+" "):] == middleBar+" ":
            msgOutput = msgOutput[:-len(middleBar+" ")]
          if "\v " in msgOutput[-2:]:
            msgOutput = msgOutput[:-2]
          if "\v" in msgOutput[-2:]:
            msgOutput = msgOutput[:-1]
          if not hideOutside:
            msgOutput = topBar + " "+ msgOutput + " " +bottomBar 
          msgOutput = msgOutput.replace("\\n", "\v").replace("\\v", "\v")
        msgGen(a)
      elif afk:
        msgOutput = topBar+a+" "+bottomBar
      else:
        msgOutput = a
      if playMsg:
        if (str(msgOutput) != lastSent) or (not suppressDuplicates) or sentTime > 30:
          client.send_message("/chatbox/input", [ str(msgOutput), True, False])
          lastSent = str(msgOutput)
          sentTime = 0
          sendSkipped = False
        else:
          sendSkipped = True
      msgDelayMemory = message_delay
      for x in range(int(message_delay*10)):
        if not playMsg or not run or ((msgDelayMemory != message_delay) and sendASAP) or sendSkipped == True:
          break
        time.sleep(.1)

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
    global useHR
    if (useHR or avatarHR) and (playMsg or avatarHR):
      if not hrConnected:
        try:
          ws = create_connection("wss://dev.pulsoid.net/api/v1/data/real_time?access_token="+pulsoidToken+"&response_mode=text_plain_only_heart_rate")
          ws.settimeout(.4)
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
                    time.sleep(.01)
                  if not run or not hrConnected:
                      break
          pulsoidListenThread = Thread(target=pulsoidListen)
          pulsoidListenThread.start()
          def blinkHR():
            global blinkThread
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
          #print('Pulsoid Connection Started...')
          outputLog('Pulsoid Connection Started...')
        except Exception as e:
          if windowAccess != None:
            if playMsg:
              windowAccess.write_event_value('pulsoidError', e)
    if ((not useHR and not avatarHR) or not (playMsg or avatarHR)) and hrConnected:
      hrConnected = False
      #print('Pulsoid Connection Stopped')
      outputLog('Pulsoid Connection Stopped')
    time.sleep(.3)
pulsoidConnectionThread = Thread(target=hrConnectionThread).start()

def spotifyConnectionCheck():
  global spotifyPlayState
  while run:
    if playMsg and "song(" in layoutString and useSpotifyApi and windowAccess != None:
      try:
        if spotifyAccessToken == '':
          raise Exception('Spotify access token missing!\nCheck output tab for more details...')
        spotifyPlayState = getSpotifyPlaystate()
      except Exception as e:  
        spotifyPlayState = ''
        windowAccess.write_event_value('spotifyApiError', e) 
    for x in range(4): #This sets the polling rate of the spotify api!!!
      if run:
        time.sleep(1)
spotifyConnectionThread = Thread(target=spotifyConnectionCheck).start()
def linkSpotify():
  outputLog('Begin Spotify Linking...')
  global spotify_client_id
  global spotify_redirect_uri
  global checkForCancel
  global NameToReturn
  global spotifyAccessToken
  global spotifyRefreshToken
  app = Flask(__name__)
  server = make_server('127.0.0.1', 8000, app)

  code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
  code_verifier = code_verifier.rstrip('=')

  code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
  code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
  code_challenge = code_challenge.replace('=', '')

  auth_url = 'https://accounts.spotify.com/authorize'
  params = {
      'client_id': spotify_client_id,
      'response_type': 'code',
      'scope': "user-read-playback-state, user-read-currently-playing",
      'redirect_uri': spotify_redirect_uri,
      'code_challenge_method': 'S256',
      'code_challenge': code_challenge
  }
  spotify_auth_url = requests.Request('GET', auth_url, params=params).prepare().url

  @app.route('/callback')


  def callback():
      global authCode
      global spotifyAccessToken
      global spotifyRefreshToken
      global checkForCancel
      global nameToReturn
      code = request.args.get('code')
      #print('Authorization code:', code)
      authCode = code
      
          
      def getAccessToken(code):
          global spotifyRefreshToken
          token_url = 'https://accounts.spotify.com/api/token'
          data = {
              'grant_type': 'authorization_code',
              'code': code,
              'redirect_uri': spotify_redirect_uri,
              'client_id': spotify_client_id,      
              'code_verifier': code_verifier
          }
          response = requests.post(token_url, data=data)
          spotifyRefreshToken = response.json().get('refresh_token')
          return response.json().get('access_token')

      spotifyAccessToken = getAccessToken(code)
      with open('spotifyCreds.txt', 'w', encoding="utf-8") as f:
          writeList = [spotifyRefreshToken, spotifyAccessToken]
          f.write(str(writeList))
      #print('Access token:', accessToken)
      
      def get_profile(accessToken):
          headers = {
              'Authorization': 'Bearer ' + accessToken,
          }

          response = requests.get('https://api.spotify.com/v1/me', headers=headers)
          data = response.json()
          return data
      profile = get_profile(spotifyAccessToken)
      def shutdown():
        server.shutdown()
      shutdownThread = Thread(target=shutdown).start()
      nameToReturn = profile.get('display_name')
      outputLog("Spotify linked to "+nameToReturn+" successfully!")
      
      return """<!DOCTYPE html> <html> <head> <title>OSC Chat Tools | Spotify Authorization</title> <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> </head> <body> <style> body { font-family: sans-serif; background-color: darkslategrey; color: whitesmoke; } .mainbox { position: absolute; left: 50%; top: 50%; -webkit-transform: translate(-50%, -50%); transform: translate(-50%, -50%); } h1 { text-align: center; } p { text-align: center; } img { display: block; margin-left: auto; margin-right: auto; width: 50%; } </style> <div class="mainbox"> <img src="https://raw.githubusercontent.com/Lioncat6/OSC-Chat-Tools/main/oscicon.ico"> <h1 class="maintext">Authorization Successful</h1><p class="subtext">You can now close this tab and return to OCT</p> <div><p>Linked to:<b style="color:green;"> """+profile.get('display_name')+""" </b></p</div> </div> </body> </html>"""
  webbrowser.open_new(spotify_auth_url)
  
  def spotifyLinkCancelCheck():
    global checkForCancel
    checkForCancel = True
    global cancelLink
    while checkForCancel:
      time.sleep(.1)
      if cancelLink:
        outputLog("Spotify linking canceled by user")
        server.shutdown()
        checkForCancel = False
        cancelLink = False
        break
  spotifyLinkCancelCheckThread= Thread(target=spotifyLinkCancelCheck).start()
  server.serve_forever()
  checkForCancel = False 
  return nameToReturn
def runmsg():
  global textParseIterator
  global playMsg
  global afk
  global FileToRead
  global scrollText
  while playMsg:
    if not afk and not scrollText:
      for x in processMessage(messageString):
        if afk or scrollText or (not playMsg):
          break
        if x == "*":
          sendMsg(" ㅤ")
        else:
          sendMsg(" "+x)
    elif afk:
      sendMsg('AFK')
      sendMsg('ㅤ')
    elif scrollText:
      try:
        fileToOpen = open(FileToRead, "r", encoding="utf-8")
        fileText = fileToOpen.read()
        if textParseIterator + 144 < len(fileText):
          sendMsg(fileText[textParseIterator:textParseIterator+144])
          textParseIterator = textParseIterator +144
        else: 
          sendMsg(fileText[textParseIterator:textParseIterator+len(fileText)-textParseIterator])
          textParseIterator = 0
      except Exception as e:
        windowAccess.write_event_value('scrollError', e)
        sendMsg('')
    else:
      sendMsg('')
  textParseIterator = 0
  if sendBlank:
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
    time.sleep(.5) 
    
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


def vrcRunningCheck():
  global vrcPID
  global playTimeDat
  def pid_check(pid):
    try:
      if psutil.pid_exists(vrcPID):
        return True
      else:
        return False
    except:
      return False
  while run:
    if not pid_check(vrcPID): 
      vrcPID = None
      for proc in psutil.process_iter():
          if "VRChat.exe" in proc.name():
              vrcPID = proc.pid
              break
          time.sleep(.01)
      playTimeDat = time.mktime(time.localtime(psutil.Process(vrcPID).create_time()))
    time.sleep(1)

vrcRunningCheckThread = Thread(target=vrcRunningCheck)
vrcRunningCheckThread.start()
msgThread = Thread(target=runmsg)
msgThread.start()
mainUI = Thread(target=uiThread)
mainUI.start()
update_checker(False)
while run:
  msgPlayCheck()
  afkCheck()
  time.sleep(.01)
