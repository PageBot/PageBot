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

import traceback
from sys import platform
from pagebot.contexts.flatcontext.flatcontext import FlatContext
from pagebot.contexts.sketchcontext.sketchcontext import SketchContext
from pagebot.contexts.markup.htmlcontext import HtmlContext
from pagebot.contexts.markup.svgcontext import SvgContext

hasDrawBot = False
DrawBotContext = None
DEFAULT_CONTEXT = None
DEFAULT_CONTEXT_TYPE = 'Flat'
CONTEXT_TYPE = None

if platform == 'darwin':

    try:
        import drawBot
        hasDrawBot = True
    except ImportError:
        hasDrawBot = False

    if hasDrawBot:
        try:
            from pagebotosx.contexts.drawbotcontext.drawbotcontext import DrawBotContext
        except ImportError:
            print(traceback.format_exc())


def getContext(contextType=None):
    """Determines which context is used:
     * DrawBotContext --> 'DrawBot'
     * FlatContext --> 'Flat'
     * HtmlContext --> 'Html'
     * InDesignContext --> 'InDesign'
     * SvgContext --> 'Svg'
     * SketchContext --> 'Sketch'

    NOTE: the global DEFAULT_CONTEXT sets the last loaded context to default
    for caching purposes. Switching context type will reload it.

    NOTE: See doctests/contexts-linux.txt and doctests/context-osx.txt for
    # platform-specific testing of contexts.
    """
    global DEFAULT_CONTEXT, CONTEXT_TYPE

    if contextType is None:
        if platform == 'darwin':
            contextType = 'DrawBot'
        else:
            contextType = 'Flat'

    if CONTEXT_TYPE and contextType != CONTEXT_TYPE:
        # Switching contexts, so resetting the buffered global object.
        DEFAULT_CONTEXT = None


    if DEFAULT_CONTEXT is None:
        if platform == 'darwin':
            if contextType == 'DrawBot' and hasDrawBot:# and DrawBotContext is not None:
                DEFAULT_CONTEXT = getDrawBotContext()
            elif contextType == 'DrawBot' and not hasDrawBot:
                print('Cannot find the pagebotosx module.')
                print('Using Flat instead of DrawBot.')
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'Flat':
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'Sketch':
                DEFAULT_CONTEXT = getSketchContext()
            elif contextType == 'Html':
                DEFAULT_CONTEXT = getHtmlContext()
            elif contextType == 'svg':
                DEFAULT_CONTEXT = getSvgContext()

        else:
            if contextType in ('DrawBot', 'Sketch'):
                print('DrawBot is not available on platform %s.' % platform)
                print('Using Flat instead of DrawBot.')
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'Flat':
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'Html':
                DEFAULT_CONTEXT = getHtmlContext()
            elif contextType == 'svg':
                DEFAULT_CONTEXT = getSvgContext()

        CONTEXT_TYPE = contextType

    return DEFAULT_CONTEXT

def getFlatContext():
    return FlatContext()

def getDrawBotContext():
    return DrawBotContext()

def getHtmlContext():
    return HtmlContext()

def getSvgContext():
    return SvgContext()

def getSketchContext():
    return SketchContext()

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
