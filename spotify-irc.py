## add a !mute function
## add a !100  function to set volume to 100
## !register <command> <uri>



# Import some necessary libraries.
import socket
import subprocess
import re


# Some basic variables used to configure the bot        
server = "irc.freenode.net" # Server
channel = "#<channel>" # Channel
botnick = "Spot-Bot" # Your bots nick

spotify = "osascript /path/to/SpotifyControl.scpt"

def ping(): # Function to respond to pings, so we don't get disconnected.
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")

def hello(): # This function responds to a user that inputs "Hello <botnick>"
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

def help():  #The help command.  This can probably be cleaned up...
	ircsock.send("PRIVMSG "+ channel +" :The currently supported commands are...\n")
	ircsock.send("PRIVMSG "+ channel +" :!play           Tells spotify to play.  Accepts arguments in the form of spotify urls/uris\n")
	ircsock.send("PRIVMSG "+ channel +" :!stop           Stops the music\n")
	ircsock.send("PRIVMSG "+ channel +" :!pause          Pauses the music\n")
	ircsock.send("PRIVMSG "+ channel +" :!next & !skip   Plays the next song\n")
	ircsock.send("PRIVMSG "+ channel +" :!prev & !last   Plays the next song\n")
	ircsock.send("PRIVMSG "+ channel +" :!shuffle        Toggles shuffle on and off\n")
	ircsock.send("PRIVMSG "+ channel +" :!repeat         Toggles repeat on and off\n")
	ircsock.send("PRIVMSG "+ channel +" :!volume N       Changes the volume.  N is substituted with a number (1 - 100)\n")
def play(n):  #Sends the play command.  Accepts arguments 
	if re.search( r'!play *\w', n):
		null, song = n.split(':!play ', 1 )
		subprocess.call(spotify + " play " + song, shell=True)
	else:
		subprocess.call(spotify + " play", shell=True)

def pause():
	subprocess.call(spotify + " pause", shell=True)

def stop():
	subprocess.call(spotify + " stop", shell=True)

def next():
	subprocess.call(spotify + " next", shell=True)

def previous():
	subprocess.call(spotify + " previous", shell=True)

def shuffle():
	subprocess.call(spotify + " shuffle", shell=True)

def repeat():
	subprocess.call(spotify + " repeat", shell=True)

def volume(n):  #Changes the volume.  Accepts arguments.  Want to add a "volume++" and "volume--" command
	if re.search( r'!volume *\w', n):
		null, level = n.split(':!volume ', 1 )
		subprocess.call(spotify + " volume " + level, shell=True)
	else:
		ircsock.send("PRIVMSG "+ channel +" :Volume requires a numeric input.  Type !help for more information.\n")

def info(): #Posts all of the spotify information about the current song
  info = subprocess.Popen(spotify + " info", shell=True, stdout=subprocess.PIPE ).communicate()[0]
  infoList = []
  infoList = output.split('\n', 10)
  pre = "PRIVMSG "+ channel +" :"
  infoList = [pre + x for x in infoList]
  for x in infoList:
    ircsock.send(x + "\n")

line = "-----------------------------------------------------------" #a variable for sexy formating. Can almost certainly be done a better way

output = subprocess.Popen(spotify + " info", shell=True, stdout=subprocess.PIPE ).communicate()[0]  #all of this is setting up for the ability to post in chat anytime the song is changed
array = []
array = output.split('\n', 10)
track = array[2]
artist = array[1]
null, track = track.split("Track:   ", 2)
null, artist = artist.split("Artist:   ", 2)

                  
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This bot is a result of a tutoral covered on http://shellium.org/wiki.\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: #Starting to listen
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  print(ircmsg) # Here we print what's coming from the server.  This is useful for debugging, and getting feedback that things are working! 
  if ircmsg.find(' PRIVMSG ')!=-1:
     nick=ircmsg.split('!')[0][1:]
     channel=ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
  

            ###################
            ## USER COMMANDS ##
            ###################
  if ircmsg.find(":Hello "+ botnick) != -1: # a "just for fun" hello command.
    hello()
  if ircmsg.find(":!play") != -1:  #sends the content of the string to the play command.  If empty, just play.  If it has an arg, go to that song
  	play(ircmsg)
  if ircmsg.find(":!pause") != -1: #sends the pause command
    pause()
  if ircmsg.find(":!stop") != -1: #sends the stop command
    stop()
  if ircmsg.find(":!next") != -1 or ircmsg.find(":!skip") != -1: #jumps to the next song
    next()
  if ircmsg.find(":!prev") != -1 or ircmsg.find(":!previous") != -1 or ircmsg.find(":!skip") != -1: #jump back to the previous song
    previous()
  if ircmsg.find(":!shuffle") != -1: #Tells spotify to toggle shuffle
    shuffle()
  if ircmsg.find(":!repeat") != -1: #Tells spotify to toggle repeat
    shuffle()
  if ircmsg.find(":!volume") != -1: #Sets the volume to be equal to the number passed in the command 
	volume(ircmsg) 
  if ircmsg.find(":!help") != -1: #lists all commands (currently hard coded...)
    help()
  if ircmsg.find(":!info") != -1: #lists all information about the current song
    info()

            #######################
            ## AUTO TRACK UPDATE ##
            #######################

  # this monitors the spotify information.  If the song changes, the bot posts to the chat with
  # the song and the artists
  output = subprocess.Popen(spotify + " info", shell=True, stdout=subprocess.PIPE ).communicate()[0]
  array = []
  array = output.split('\n', 10)
  if track != array[2]:
    track = array[2]
    artist = array[1]
    null, track2 = track.split("Track:   ", 2)
    null, artist = artist.split("Artist:   ", 2)
    ircsock.send("PRIVMSG "+ channel +" :" + line + "\n")
    ircsock.send("PRIVMSG "+ channel +" :   Now playing:" + track2 +" by " + artist + "\n")
    ircsock.send("PRIVMSG "+ channel +" :" + line + "\n")



  if ircmsg.find("PING :") != -1: # making sure to respond to server pings
    ping()