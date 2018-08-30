#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     Basics.py
#
#     Shows how use basic pagebot functions.
#    
from pagebot import *

def doBasics():
	"""
	>>> rootPath = getRootPath()
	>>> resourcesPath = getResourcesPath()
	>>> context = getContext()
	>>> print(context)
	<DrawBotContext>
	>>> context = getContext('DrawBot')
	>>> print(context)
	<DrawBotContext>
	>>> context = getContext('Flat')
	>>> print(context)
	<FlatContext>

	"""
	rootPath = getRootPath()
	print(rootPath)
	resourcesPath = getResourcesPath()
	print(resourcesPath)
	context = getContext()
	print(context)
	context = getContext('Flat')
	print(context)

doBasics()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])