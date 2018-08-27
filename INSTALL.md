# PageBot Version 0.6

## Installing

Since PageBot is not part of the standard DrawBotApp, it needs to be installed separately. 

Another reason for manual installation is that it allows updating PageBot to the latest version, while DrawBot is not updated. 
And developers may choose to run an alternative branch of PageBot to test specific functions before they are merged back into github master.

The installation process is part of the development of the library itself, so it may still not always work properly.
Here are some hints to check on installation and to install without using the *setup.py* script.

### setup.py

Run `sudo python setup.py install` to install PageBot in the default Python of the OSX.
There are some known problems here:

* The default `Python` may not be the same one that DrawBotApp uses. On some OSX systems, there are multiple versions of Python installed, in which case PageBot may be installed with a different one. DrawBot then cannot find the installed PageBot.

* Always restart DrawBotApp, as opening new libraries only takes place on startup.

* Don't move the git-repository to another location after it is installed. Python builds a reference to the libary where it is located during installation. After moving, make sure to run the initializer again.

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

If there is no error, PageBot is installed properly for this Python.

### Testing in DrawBotApp

* Open DrawBotApp
* Open a new editor window.
* Type `import pagebot`
* Presse cmd-R to run this minimalistic one-line script
* If there is no error then PageBot is installed properly for DrawBotApp.

### Install dependencies

PageBot is using other Open Source libraries that may (or may not) be already installed in RoboFont.
Also, when running PageBot outside of DrawBot context (e.g. using Flat), these libraries need to be installed separately.

* https://github.com/xxyxyz/flat
* https://github.com/typesupply/compositor
* https://github.com/imageio/imageio
* https://sass.github.io/libsass-python

https://github.com/GoogleCloudPlatform/google-cloud-python

### Install dependencies in the terminal

sudo pip install svgwrite
sudo pip install imageio
sudo pip install libsass


