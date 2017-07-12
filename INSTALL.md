# PageBot Version 0.5

## Installing

As long as PageBot is not part of the standard DrawBotApp, it needs to be installed separately. 

Another reason for manual install is that it allows to update PageBot to the latest version, when DrawBot is not updated. 
And developers may choose to run an alternative branche of PageBot to test specific functions before they are merged back into the github master.

The installing process is part of the development of the library itself, so it may not always work properly still.
Here are some hints to check on installation and to install without using the *setup.py* script.

### setup.py

Run `sudo python setup.py install` to install PageBot in the default Python of the OSX.
There are some known problems here:

* The default `Python` may not be the same one a DrawBotApp is using. On some OSX system, there are multiple versions of Python installed, in which case PageBot is installed with a different one. DrawBot then cannot find the installed PageBot.

* Always restart DrawBotApp, as opening new libraries only takes place on startup.

* Don't move the git-repository to another location, after it  is installed. Python builds a reference to the libary where it is located during installation. After moving, make sure to run the initializer again.

### Finding the installed PageBot with the Finder

Goto `/Library/Python/2.7/site-packages` in the Finder. If there a PageBot reference here, either as .pth file or a Python egg file?

* If not, then try to reinstall, there may have been (another) error during installation
* If there is a .pth file, look into it (click-space on the icon) and verify that the path is pointing to where 

### Testing in the terminal

Open a terminal

	++ python
	Python 2.7.10 (default, Feb  7 2017, 00:08:15) 
	[GCC 4.2.1 Compatible Apple LLVM 8.0.0 	(clang-800.0.34)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import pagebot
	>>> 

If there is no error, PageBot is install property for this Python.

### Testing in DrawBotApp

Open DrawBotApp
Open a new editor window.
Type
	import drawbot
Type
	cmd-R to run the "program"
If there is no error, PageBit is installed property for DrawBotApp.

