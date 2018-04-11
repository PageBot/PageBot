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

DEFAULT_CONTEXT = None
MAMP_PATH = None

def getContext():
    global DEFAULT_CONTEXT, MAMP_PATH
    if DEFAULT_CONTEXT is None:
        try:
            #import ForceImportError # Uncomment for simulate testing of other contexts/platforms
            import AppKit # Force exception on non-OSX platforms
            from pagebot.contexts.drawbotcontext import DrawBotContext
            DEFAULT_CONTEXT = DrawBotContext() # Test if platform is supporing DrawBot:
            # MampView.build exports in MAMP folder that does not commit in Git. 
            MAMP_PATH = '/Applications/MAMP/htdocs/'

        #except (ImportError, AttributeError, ModuleNotFoundError): # Python3
        except (ImportError, AttributeError):
            #import ForceOtherError # Uncomment for simulate testing of other contexts/platforms
            from pagebot.contexts.flatcontext import FlatContext
            DEFAULT_CONTEXT = FlatContext()
            # MampView.build exports in MAMP folder that does not commit in Git. 
            MAMP_PATH = '/tmp/MAMP_PATH/' # TODO: Where is it located for Linux?
        except:
            raise NotImplementedError('Cannot decide on the platform context.')
    return DEFAULT_CONTEXT

def getMampPath():
    if MAMP_PATH is None:
        getContext() # Make sure MAMP_PATH is initialized depending on current type of context.
    return MAMP_PATH
    
if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
