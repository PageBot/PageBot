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
TESTFLATONMAC = False

def getContext():
    """Determines which context is used:
     * DrawBotContext
     * FlatContext
     * InDesignContext

    """
    global DEFAULT_CONTEXT, MAMP_PATH

    if DEFAULT_CONTEXT is None:
        if platform == 'darwin' and not TESTFLATONMAC:
            try:
                # Remove comment to simulate testing on other contexts/platforms.
                #import ForceImportError
                import AppKit # Force exception on non-OSX platforms
                from pagebot.contexts.drawbotcontext import DrawBotContext
                DEFAULT_CONTEXT = DrawBotContext() # Test if platform is supporing DrawBot:
                MAMP_PATH = '/Applications/MAMP/htdocs/'
            except:
                print(traceback.format_exc())
                raise NotImplementedError('Error loading context.')
        else:
                # Remove comment to simulate testing on other contexts/platforms.
                #import ForceOtherError
                from pagebot.contexts.flatcontext import FlatContext
                DEFAULT_CONTEXT = FlatContext()
                MAMP_PATH = '/tmp/MAMP_PATH/' # TODO: Where is it located for Linux?

        # TODO: Indesign context.

    return DEFAULT_CONTEXT

def getMampPath():
    """Make sure MAMP_PATH is initialized depending on the context."""
    if MAMP_PATH is None:
        getContext()
    return MAMP_PATH

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
