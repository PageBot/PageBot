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
#     pagebot/contexts/platform.py
#
import traceback
DEFAULT_CONTEXT = None
MAMP_PATH = None
from sys import platform
#TESTFLATONMAC = False

def getContext(contextType=None):
    """Determines which context is used:
     * DrawBotContext
     * FlatContext
     * InDesignContext

    """
    global DEFAULT_CONTEXT, MAMP_PATH

    # FIXME: what about MAMP_PATH is None?
    if DEFAULT_CONTEXT is None or not contextType is None:
        if platform == 'darwin':
            if contextType == 'DrawBot' or contextType is None:
                DEFAULT_CONTEXT = getDrawBotContext()
            elif contextType == 'Flat':
                DEFAULT_CONTEXT = getFlatContext()
            '''
            elif contextType == 'InDesign':
                ...
            '''

            MAMP_PATH = '/Applications/MAMP/htdocs/'
        else:
            DEFAULT_CONTEXT = getFlatContext()
            # TODO: What's the actual path on Linux?

            MAMP_PATH = '/tmp/MAMP_PATH/'
        # TODO: Indesign context.

    return DEFAULT_CONTEXT

def getFlatContext():
    from pagebot.contexts.flatcontext import FlatContext
    return FlatContext()

def getDrawBotContext():
    from pagebot.contexts.drawbotcontext import DrawBotContext
    return DrawBotContext()

def getMampPath():
    """Make sure MAMP_PATH is initialized depending on the context."""
    if MAMP_PATH is None:
        getContext()
    return MAMP_PATH

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
