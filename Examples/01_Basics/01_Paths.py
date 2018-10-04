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
#     01_Paths.py
#
#     Shows how get pagebot paths.
#
from pagebot import *
import glob

def showPaths():
	rootPath = getRootPath()
	print(rootPath)
	resourcesPath = getResourcesPath()
	print(resourcesPath)
	print(glob.glob('%s/*' % resourcesPath))
	defaultFontPath = getDefaultFontPath()
	print(defaultFontPath)
	context = getContext()
	print(context)
	context = getContext('Flat')
	print(context)

showPaths()
