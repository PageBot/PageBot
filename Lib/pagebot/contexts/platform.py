# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     pagebot/contexts/platform.py
#
import pagebot
from pagebot.toolbox.transformer import path2ParentPath

ROOT_PATH = path2ParentPath(pagebot.__file__)
RESOURCES_PATH = ROOT_PATH + '/resources'

def getRootPath():
    u"""Answer the root path on the platform for the PageBot module."""
    return ROOT_PATH

def getResourcesPath():
    u"""Answer the root path on the platform for the PageBot module."""
    return RESOURCES_PATH

#   C O N T E X T S

DEFAULT_CONTEXT = None

def getContext():
    global DEFAULT_CONTEXT
    if DEFAULT_CONTEXT is None:
        try:
            #import ForceImportError # Uncomment for simulate testing of other contexts/platforms
            import AppKit # Force exception on non-OSX platforms
            from pagebot.contexts.drawbotcontext import DrawBotContext
            DEFAULT_CONTEXT = DrawBotContext() # Test if platform is supporing DrawBot:

        #except (ImportError, AttributeError, ModuleNotFoundError): # Python3
        except (ImportError, AttributeError):
            #import ForceOtherError # Uncomment for simulate testing of other contexts/platforms
            from pagebot.contexts.flatcontext import FlatContext
            DEFAULT_CONTEXT = FlatContext()
        except:
            raise NotImplementedError('Cannot decide on the platform context.')
    return DEFAULT_CONTEXT

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
