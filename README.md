spotify-irc-bot
===============

An IRC bot that can send commands via terminal to Spotify using https://github.com/dronir/SpotifyControl

Version 0.0.2 (3-26-14):

* New Features
	* Added the ability to register aliases for songs/playlists/etc.
		* Syntax is "!register <alias> <uri>"
	* Added the ability to play registered aliases 
		* Syntax is "~<alias>"
	* Added a check so that unregistered aliases will tell the users that alias is not registered.
	* The aliases are stored in .pickle file.  An example file has been included in this commit.
	* !shuffle will now let you know whether Shuffle is true or false.
	* Added a "Now Playing" feature. This *should* update every time the song changes.
	* Squashed a couple bugs
	* Added to !info


* Known bugs
	* Typing !volume or !play with content after, but no spaces, will crash the bot
		* (for example !playy)
	* The auto-update feature for "Now Playing" doesn't always fire immediately.  
	* The alternate commands for next and previous don't seem to work right now.