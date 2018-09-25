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
import glob

def doBasics():
	rootPath = getRootPath()
	print(rootPath)
	resourcesPath = getResourcesPath()
	print(resourcesPath)
	print(glob.glob('%s/*' % resourcesPath))
	context = getContext()
	print(context)
	context = getContext('Flat')
	print(context)

doBasics()