#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     __init__.py
#

from sys import platform
import re
from pagebot.filepaths import *
from pagebot.contexts import getContext as getPlatformContext
from pagebot.contexts import getContextMampPath
from pagebot.fonttoolbox.objects.font import findFont

VERSION = '0.9.8'
STATUS = 'alpha'
__doc__ = """PageBot module"""
__version__ = '%s-%s' % (VERSION, STATUS)

contextTypes = ('DrawBot', 'Flat', 'HTML', 'svg')#, 'InDesign', 'idml')

def getRootPath():
    """Answers the root path of the PageBot module for the current platform."""
    return ROOT_PATH

def getResourcesPath():
    """Answers the resources path within the PageBot module for the current
    platform."""
    return RESOURCES_PATH

def getDefaultFontPath():
    """Answers the default font path within the PageBot module for the current
    platform."""
    return DEFAULT_FONT_PATH

def getContext(contextType=None):
    """Returns a single context."""

    # Sets the default for both supported platforms.
    if contextType is None:
        if platform == 'linux':
            contextType = 'Flat'
        elif platform == 'darwin':
            contextType = 'DrawBot'

    return getPlatformContext(contextType=contextType)

def getContexts(types):
    """Returns multiple contexts, contextTypes should be specified as a
    list."""
    contexts = []

    for contextType in types:
        context = getPlatformContext(contextType=contextType)
        contexts.append(context)

    return contexts

def getAllContexts():
    """Returns all available contexts."""
    contexts = []

    for contextType in contextTypes:
        contexts.append(getPlatformContext(contextType=contextType))
    return contexts

def getFontByName(name):
    return findFont(name)

def getMampPath():
    return getContextMampPath()

'''
In order to let PageBot scripts and applications exchange information without
the need to save data in files, the pbglobals module provides the storage of
non-persistent information. This way, on OSX, applications with Vanilla windows
can be used as UI for scripts that perform as batch process.

Note that the individual scripts need to create unique ID's for attributes.
Also they need to know of each other, in case information is exchanged.

The key is the script or application ID, e.g. their __file__ value.

Access as:

  from pagebot.toolbox.transformer import path2ScriptId
  scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))

or directly as:

...
'''

pbGlobals = {}

class Globals:
    # Allow adding by attribute and key.
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

def getGlobals(scriptId):
    """In order to let PageBot scripts and applications exchange information,
    without the need to save as files, the pbglobals module supports the
    storage of non-persistent information. This way, applications with Vanilla
    windows can be used as UI for scripts that perform as batch process.  Note
    that it is up to the responsibilty of individual scripts to create uniqued
    ids for attributes. Also they need to know from each other, in case
    information is exchanged."""
    if not scriptId in pbGlobals:
        pbGlobals[scriptId] = Globals()
    return pbGlobals[scriptId]

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
