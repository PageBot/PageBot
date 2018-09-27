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
#     pagebot/contexts/__init__.py
#

DEFAULT_CONTEXT = None
CONTEXT_TYPE = None
MAMP_PATH = None
from sys import platform

def getContext(contextType='DrawBot'):
    """Determines which context is used:
     * DrawBotContext
     * FlatContext
     * HtmlContext
     * InDesignContext

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
            elif contextType == 'HTML':
                DEFAULT_CONTEXT = getHtmlContext()
            elif contextType == 'InDesign':
                '''
                To be implemented.
                '''

            MAMP_PATH = '/Applications/MAMP/htdocs/'
        else:
            if contextType in ('DrawBot', 'InDesign'):
                print('drawbot context not available')
                # TODO: raise error
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'Flat':
                DEFAULT_CONTEXT = getFlatContext()
            elif contextType == 'HTML':
                DEFAULT_CONTEXT = getHtmlContext()

            # TODO: What's the actual path on Linux?
            MAMP_PATH = '/tmp/MAMP_PATH/'

        CONTEXT_TYPE = contextType

    return DEFAULT_CONTEXT

def getFlatContext():
    from pagebot.contexts.flatcontext import FlatContext
    return FlatContext()

def getDrawBotContext():
    from pagebot.contexts.drawbotcontext import DrawBotContext
    return DrawBotContext()

def getHtmlContext():
    from pagebot.contexts.htmlcontext import HtmlContext
    return HtmlContext()

def getMampPath():
    """Make sure MAMP_PATH is initialized depending on the context."""
    if MAMP_PATH is None:
        getContext()
    return MAMP_PATH

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
