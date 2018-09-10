# Installing PageBot

## Testing

To help with the installation of PageBot, there's an example script to test versions, locations and dependencies:

    Examples/000_Installing/TestInstall.py
    
This can be run from DrawBot, Sublime or on the command line to find out if you have all the components in place to start using PageBot.

## setup.py

Run `sudo python3 setup.py install` to start installing PageBot. When setup is finished, you should see the files in one of your `site-packages` or `dist-packages` locations. Using the `site` module, you can find out what 

    import site
    
    print('Found site at %s' % site.__file__)
    packages = site.getsitepackages()
    for p in packages:
        print(' - %s' % p)

For example, in Sublime:

 - /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages
 - /Library/Python/3.6/site-packages

And DrawBot:

 - /Applications/DrawBotPy3.app/Contents/Resources/lib/python3.6/site-packages
 - /Library/Python/3.6/site-packages

## Dependencies

PageBot needs other Open Source libraries. Some may already be included in DrawBot.

* https://github.com/TypeNetwork/flat
* https://github.com/typesupply/compositor
* https://github.com/imageio/imageio
* https://sass.github.io/libsass-python


## Notes

* PageBot now runs entirely on Python 3 and DrawBotApp 3. Python 2.7 is no longer supported. We have ported the flat library to Python 3 and are currently maintaining it at https://github.com/TypeNetwork/flat.

* The default `Python` may not be the same one that DrawBotApp uses. On some OSX systems, there are multiple versions of Python installed, in which case PageBot may be installed with a different one. DrawBot then cannot find the installed PageBot.

* DrawBotApp should be restarted after installation because libraries are scanned at startup.

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

### Install dependencies in the terminal

sudo pip install svgwrite
sudo pip install imageio
sudo pip install libsass


