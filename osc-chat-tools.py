#######################################################################################
#CONFIG SETTINGS:

#1 time + specs + song
#2 time + song
#3 song
#4 time
#5 message Script
#6 Message + time
#7 AFK
#8 Just Message
#9 Text File Parser
#10 Song + msg
DisplayMode = 10

#File path of the file to read 
FileToRead = 'test.txt'

#Message to display for all of the above message options
#To add a new animation frame (each one is 1.5s) wrap your text with `sendMsg('<MESSAGE>')`
def msgConf(): #Leave This Line Alone! 
  sendMsg('Test frame one')
  sendMsg('Test frame two')
  sendMsg('Test frame three')
#CONFIG END  
#######################################################################################
import os
import time
from threading import Thread

if not os.path.isfile('please-do-not-delete.txt'):
  os.system("pip install python-osc")
  os.system("pip install argparse")
  os.system("pip install datetime")
  os.system("pip install keyboard")
  os.system("pip install asyncio")
  os.system("pip install psutil")
  with open('please-do-not-delete.txt', 'w') as f:
      f.write('This File is for osc chat tools by lioncat6. This file marks that the necessary python modules have been installed in order for this script to run. Please do not delete it unless you are troubleshooting an issue.')

import argparse
from datetime import datetime
from pythonosc import udp_client
import keyboard
import asyncio
import psutil

from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

playMsg = True
cpuInt = int(psutil.cpu_percent(.1)*10)
textParseIterator = 0


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
    if playMsg:
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
      
      
      #song shit \/
      current_media_info = asyncio.run(get_media_info())
      songInfo="🎵"+current_media_info['title']+" by "+current_media_info['artist']+"🎵"
      letsGetThatTime =str(current_hour)+":"+current_minute+dayThing
      if DisplayMode == 1:
        part1= "╔═════════════╗ "+letsGetThatTime+" Cpu: "+ str(int(psutil.cpu_percent(.1)*10))+"% Ram: "+str(int(psutil.virtual_memory()[2]))+"% ╠═════════════╣ "
      elif DisplayMode ==2 or DisplayMode == 6:
        part1= "╔═════════════╗ "+letsGetThatTime+"  ╠═════════════╣ "
      elif DisplayMode ==3 or DisplayMode ==5 or DisplayMode ==7 :
        part1= "╔═════════════╗ "
      else: 
        part1= "╔═════════════╗ "+letsGetThatTime
      if DisplayMode == 4 or DisplayMode ==7:
        part2= " ╚═════════════╝"
        client.send_message("/chatbox/input", [ part1+a+part2, True, False])
      elif DisplayMode == 5 or DisplayMode == 6:
        part2= " "+"╚═════════════╝"
        client.send_message("/chatbox/input", [ part1+a+part2, True, False])
      elif DisplayMode == 8 or DisplayMode == 9:
        client.send_message("/chatbox/input", [ a, True, False])
      elif DisplayMode == 10:
        part1= "╔═════════════╗ "+a+"  ╠═════════════╣ "
        part2= "Listening To: "+songInfo+"ㅤ╚═════════════╝"
        client.send_message("/chatbox/input", [ part1+part2, True, False])
      else:
        part2= "Listening To: "+songInfo+"ㅤ╚═════════════╝"
        client.send_message("/chatbox/input", [ part1+part2, True, False])
      
      #print(part1+a+part2)
      if DisplayMode == 9:
        for x in range(60):
          time.sleep(.1)
          if not playMsg:
            break
      else:
        for x in range(15):
          time.sleep(.1)
          if not playMsg:
            break

def runmsg():
  global textParseIterator
  global playMsg
  while playMsg:
    if DisplayMode == 1 or DisplayMode == 2 or DisplayMode == 3 or DisplayMode == 5 or DisplayMode == 6 or DisplayMode ==8 or DisplayMode ==10:
      msgConf()
    elif DisplayMode == 7:
      sendMsg('AFK')
      sendMsg('ㅤ')
    elif DisplayMode == 9:
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
    
  client.send_message("/chatbox/input", [ " ", True, False])
    
def msgPlayCheck():
  global playMsg
  if keyboard.is_pressed('p'):
    if playMsg:
      playMsg = False
      time.sleep(.5)
    else:
      playMsg = True  
      msgThread = Thread(target=runmsg)
      msgThread.start()
      time.sleep(.5) 

def restartMsg():
  global playMsg
  playMsg = False
  time.sleep(1.5)
  playMsg = True  
  msgThread = Thread(target=runmsg)
  msgThread.start()

def confCheck():
  global DisplayMode
  if keyboard.is_pressed('['):
    if DisplayMode <=9:
      DisplayMode = DisplayMode + 1
      #restartMsg()
      time.sleep(.3)
    else:
      DisplayMode = 1
      #restartMsg()
      time.sleep(.3)
msgThread = Thread(target=runmsg)
msgThread.start()
while True:
  msgPlayCheck()
  confCheck()
  time.sleep(.01)