# PageBot Version 0.6

## Installing



### setup.py

Run `sudo python3 setup.py install` to start installing PageBot. When setup is finished, you should see the files in your `site-packages` or `dist-packages` folder. For example,

    /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages


 Some notes:

* PageBot now runs entirely on Python 3 and DrwaBotApp 3. Python 2.7 is no longer supported.

* The default `Python` may not be the same one that DrawBotApp uses. On some OSX systems, there are multiple versions of Python installed, in which case PageBot may be installed with a different one. DrawBot then cannot find the installed PageBot.

* Always restart DrawBotApp, as opening new libraries only takes place on startup.

* Don't move the git-repository to another location after it is installed. Python builds a reference to the libary where it is located during installation. After moving, make sure to run the initializer again.

### Finding the installed PageBot with the Finder

Goto `/Library/Python/3.6/site-packages` in the Finder. If there a PageBot reference here, either as .pth file or a Python egg file?

* If not, then try to reinstall, there may have been (another) error during installation
* If there is a .pth file, look into it (click-space on the icon) and verify that the path is pointing to where the PageBot repository is located.

### Testing in the terminal

Open a terminal

~~~Python3
++ python3
Python 3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pagebot
>>> 
~~~

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


