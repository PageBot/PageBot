#!/usr/bin/env python3
# -*- coding: UTF-8 -*- # ----------------------------------------------------------------------------- #
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
import os.path
from pagebot.constants import DEFAULT_FONT
from pagebot.contexts import getContext as getPlatformContext
from pagebot.fonttoolbox.objects.font import findFont

VERSION = '1.0.2'

__doc__ = """PageBot module"""
__version__ = '%s' % VERSION

contextTypes = ('flat', 'html', 'svg')
contextTypesOSX = ('drawbot',)

def getContext(contextType=None, resourcesPath=None):
    """Returns a single context."""

    # Sets the default for both supported platforms.
    if contextType is None:
        if platform == 'linux':
            contextType = 'flat'
        elif platform == 'darwin':
            contextType = 'drawbot'
        else:
            raise NotImplementedError

    return getPlatformContext(contextType=contextType)

def getContexts(types):
    """Returns multiple contexts, contextTypes should be specified as a
    list.


    >>> getContexts(['Flat', 'HTML'])
    [<FlatContext>, <HtmlContext>]
    """
    contexts = []

    for contextType in types:
        context = getPlatformContext(contextType=contextType)
        contexts.append(context)

    return contexts

def getAllContexts():
    """Returns all available contexts.

    >>> allContext = getAllContexts()
    """
    contexts = []

    for contextType in contextTypes:
        contexts.append(getPlatformContext(contextType=contextType))
    if platform == 'darwin':
        for contextType in contextTypesOSX:
            contexts.append(getPlatformContext(contextType=contextType))

    return contexts

def getFontByName(name):
    """
    >>> getFontByName('PageBot')
    """
    return findFont(name)

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
    """
    >>> g = Globals()
    >>> g['bla'] = 'bla'
    """

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
    information is exchanged.

    >>> g = getGlobals('testScriptID')
    """
    if not scriptId in pbGlobals:
        pbGlobals[scriptId] = Globals()
    return pbGlobals[scriptId]

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
