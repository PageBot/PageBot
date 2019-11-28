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
from pagebot.contexts.flatcontext.flatcontext import FlatContext
from pagebot.contexts.markup.htmlcontext import HtmlContext
from pagebot.contexts.markup.svgcontext import SvgContext

DrawBotContext = None
CanvasContext = None

if platform == 'darwin':
    try:
        # TODO: check if drawBotContext exists first, ask to install.
        from pagebotcocoa.contexts.drawbot.drawbotcontext import DrawBotContext
        from pagebotcocoa.contexts.canvas.canvascontext import CanvasContext
    except:
        print('Please install pagebotcocoa.')
        print('pip install pagebotcocoa')

DEFAULT_CONTEXT = None
CONTEXT_TYPE = None
MAMP_PATH = None

def getContext(contextType='DrawBot'):
    """Determines which context is used:
     * DrawBotContext
     * FlatContext
     * HtmlContext
     * InDesignContext
     * SvgContext

    NOTE: the global DEFAULT_CONTEXT sets the last loaded context to default
    for caching purposes. Switching context type will reload it.
    """
    global DEFAULT_CONTEXT, MAMP_PATH, CONTEXT_TYPE

    if CONTEXT_TYPE and contextType != CONTEXT_TYPE:
        # Switching contexts, so resetting the buffered global object.
        DEFAULT_CONTEXT = None

    # FIXME: what about MAMP_PATH is None?
    # FIXME: what about HTMLContext()
    if DEFAULT_CONTEXT is None:
        if platform == 'darwin':
            if contextType == 'DrawBot':
                DEFAULT_CONTEXT = getDrawBotContext()
            elif contextType == 'Flat':
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'Canvas':
                DEFAULT_CONTEXT = getCanvasContext()
            elif contextType == 'HTML':
                DEFAULT_CONTEXT = getHtmlContext()
            #elif contextType == 'InDesign':
            #    DEFAULT_CONTEXT = getInDesignContext()
            #elif contextType == 'idml':
            #    DEFAULT_CONTEXT = getIdmlContext()
            elif contextType == 'svg':
                DEFAULT_CONTEXT = getSvgContext()
            #elif contextType == 'SVG':
            #    DEFAULT_CONTEXT = getSvgContext()

            MAMP_PATH = '/Applications/MAMP/htdocs/'
        else:
            if contextType in ('DrawBot',):
                print('Selected context type is not available on this platform: %s for %s' % (contextType, platform))
                # TODO: raise error
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'Flat':
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'HTML':
                DEFAULT_CONTEXT = getHtmlContext()
            #elif contextType == 'InDesign':
            #    DEFAULT_CONTEXT = getInDesignContext()
            #elif contextType == 'idml':
            #    DEFAULT_CONTEXT = getIdmlContext()
            elif contextType == 'svg':
                DEFAULT_CONTEXT = getSvgContext()

            # TODO: What's the actual path on Linux?
            MAMP_PATH = '/tmp/MAMP_PATH/'

        CONTEXT_TYPE = contextType

    return DEFAULT_CONTEXT

def getFlatContext():
    return FlatContext()

def getDrawBotContext():
    if platform != 'darwin':
        return None

    return DrawBotContext()

def getCanvasContext():
    if platform != 'darwin':
        return None

    return CanvasContext()

def getHtmlContext():
    return HtmlContext()

#def getIdmlContext():
#    return IdmlContext()

def getSvgContext():
    return SvgContext()

def getContextMampPath():
    """Make sure MAMP_PATH is initialized depending on the context."""
    if MAMP_PATH is None:
        getContext()
    return MAMP_PATH

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
