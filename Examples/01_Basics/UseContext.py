from pagebot import getContext

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
#     UseContext.py
#
#     Shows how to get different types of contexts.


def showContexts():
	print('Here are some examples of how to retrieve different kinds of contexts:')
	context = getContext() # Creates a DrawBot context on Mac, Flat on others
	print(context)
	context = getContext() # Still DrawBot, takes the buffered DEFAULT_CONTEXT.
	print(context)
	context = getContext('DrawBot') # Still DrawBot, takes the buffered DEFAULT_CONTEXT.
	print(context)
	context = getContext(contextType='Flat') # Force Flat.
	print(context)
	context = getContext(contextType='Flat') # Buffered in DEFAULT_CONTEXT this time.
	print(context)
	context = getContext(contextType='HTML')
	print(context)
	context = getContext(contextType='InDesign') # To be implemented.
	print(context)
	context = getContext(contextType='SVG') # To be implemented.
	print(context)


showContexts()
