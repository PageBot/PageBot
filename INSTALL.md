# Installing PageBot

# Setup

Run `sudo python3 setup.py install` to start installing PageBot. If all goes well, the setup will finish without errors while printing out the location of the files:

	...
	creating dist
	creating 'dist/pagebot-0.6-py3.6.egg' and adding 'build/bdist.macosx-10.6-intel/egg' to it
	removing 'build/bdist.macosx-10.6-intel/egg' (and everything under it)
	Processing pagebot-0.6-py3.6.egg
	creating <path-to>/site-packages/pagebot-0.6-py3.6.egg
	Extracting pagebot-0.6-py3.6.egg to <path-to>/site-packages
	Adding pagebot 0.6 to easy-install.pth file

## Site-packages

You should see the files created in one of your `site-packages` or `dist-packages` locations now. Note: The default version of Python 3 may not be the same one that DrawBotApp uses. On some macOS systems, there are multiple versions of Python installed, in which case PageBot may be installed with a different one. In that case DrawBot cannot only find the installed PageBot if it has been installed in the shared `site-packages` folder.

The `getsitepackages()` function can be used to get more information on installation paths. DrawBot has an internal packages folder containing it's own dependencies. The packages path might differ across platforms. An example:

    import site
    
    print('Found site at %s' % site.__file__)
    packages = site.getsitepackages()
    for p in packages:
        print(' - %s' % p)

On the command line, this might give:

 - /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages
 - /Library/Python/3.6/site-packages

And inside DrawBot:

 - /Applications/DrawBotPy3.app/Contents/Resources/lib/python3.6/site-packages
 - /Library/Python/3.6/site-packages

NOTE: the `site.py` file in `/Applications/DrawBotPy3.app/Contents/Resource` needs to be renamed to something else before the `import site` line gives the correct results.


## Dependencies

PageBot needs other Open Source libraries. Some may already be included in DrawBot, but need to be installed separately for system-wide use.

* https://github.com/fonttools/fonttools
* https://pypi.org/project/pyobjc/ (OS X only, included in DrawBot)
* https://github.com/typesupply/vanilla (OS X only, included in DrawBot)
* https://github.com/PageBot/flat (not needed when using DrawBot only)
* https://sass.github.io/libsass-python

To install them, you can use a package manager such as `pip`, `easy_install` or `homebrew` or you can do it manually by downloading them from the Python Index and running the setup scripts.

## Notes

* PageBot now runs entirely on Python 3 and DrawBotApp 3. Python 2.7 is no longer supported. We have ported the flat library to Python 3 and are currently maintaining it at https://github.com/PageBot/flat.

* The default `Python` may not be the same one that DrawBotApp uses. On some OSX systems, there are multiple versions of Python installed, in which case PageBot may be installed with a different one. DrawBot then cannot find the installed PageBot.

* DrawBotApp should be restarted after installation because libraries are scanned at startup.

Go to `/Library/Python/2.7/site-packages` in the Finder.
Is there a PageBot reference here, either as `.pth` file or a Python egg file?
* If not, then try to reinstall, there may have been (another) error during installation.
* If there is a `.pth` file, look into it (click-space on the icon) and verify that the path is pointing to your PageBot folder path.
* Don't move the git-repository to another location after it is installed. Python builds a reference to the libary where it is located during installation. After moving, make sure to run the initializer again.

## Checking

### On the Terminal

Open a terminal, and run the python command

~~~Python3
++ python3
Python 3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pagebot
>>> 
~~~

You should see the python command prompt:

    Python 2.7.10 (default, Feb  7 2017, 00:08:15) 
    [GCC 4.2.1 Compatible Apple LLVM 8.0.0 	(clang-800.0.34)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Then run the `import pagebot` command.
If there is no error, PageBot is installed properly for this Python, and it will look like this:
	
    >>> import pagebot
    >>> 

### In DrawBotApp

* Open DrawBotApp
* Open a new editor window.
* Type `import pagebot`
* Press cmd-R to run the script

If there is no error then PageBot is installed properly.

### In Sublime


Sublime needs to be configured to build with Python 3 first. An example configuration file can be found here:

	Patches/Python3.sublime-build
	
The first line should contain the path to the python3 executable:

	{
	  "cmd": ["/<path>/<to>/python3", "$file"], 
	  "selector": "source.python", 
	  "file_regex": "file \"(...*?)\", line ([0-9]+)"
	}

You can find out the path by using the `which` command:

	which python3
	
After the path is set, the sublime-build file should be moved to:

	/Users/<username>/Library/Application Support/Sublime Text 3/Packages/User

After restarting Sublime, you should be able to select the Python3 option in the Build System list. Select it and run `import pagebot` by typing cmd-B.

## Testing

To help with the installation of PageBot, we've provided an example script to test versions, locations and dependencies:

    Examples/000_Installing/TestInstall.py
    
The script can be run from DrawBot, Sublime or on the command line to find out if all the components are in place to start using PageBot.

# Path File

Alternatively, for development purposes you can simply clone the PageBot repository somewhere and link to the sources in Lib using a path file ('.pth'). For example, a file containing

    /Users/<username>/Code/FontTools/Lib/
    /Users/<username>/Code/PageBot/Lib/
    
will reference to the `fontTools` and `pagebot` modules provided they have been cloned there from GitHub. The name of the file doesn't matter as long as it ends with `.pth` and is located in one of the `site-packages` locations.

The advantage of this approach is that you will be up to date to the latest commit as long as you keep syncing. Make sure there's no previously installed version in one of your `site-packages` folders. Check the path of the pagebot module after importing it to make sure it is correct:

	Python 3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28) 
	[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import pagebot
	>>> print(pagebot)
	<module 'pagebot' from '/Users/<username>/Code/PageBot/Lib/pagebot/__init__.py'>


If the module references the package or egg-file inside `site-packages`, you might need to remove the previously installed version like this:

	pip3 uninstall pagebot

If `pip` hasn't indexed the module, you can simply delete the files.

