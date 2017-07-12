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

### MORE HERE SOON

