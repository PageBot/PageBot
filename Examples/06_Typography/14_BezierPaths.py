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
#     14_BezierPaths.py
#
#     This script shows the behavior and functions of BezierPaths as they exist 
#     the DrawBotContext. Most of the functions are directly defined by the
#     OSX defintion of BezierPaths. 
#     (Note that BezierPaths sometimes get referred to as "path", but there is
#     not relation with the often used "path" in PageBot filepaths.)
#     In DrawBotContext the BezierPath is an integral part of the API.
#     TODO: FlatContext should copy this behavior. It's worthwhile to see if
#     it is possible to use the booleanOperator for the FlatContext version,
#     if the path description gets close to the code of BezierPath in DrawBot.
#
#     These example draw directly on the context canvas.
#     Look for the same examples working as BezierPathElement.py inside Document,
#     Page and Element layout usage.
#

from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em
from pagebot.constants import * # Import all constants for convenience

context = getContext()

W = H = 1000 # Document size
P = 100 # Page padding on all sides. Select value and cmd-drag to change interactive.

context.newPage(W, H)
# Dummy text, used several times to create the length we need for this example
text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

font = findFont('Roboto-Regular')

# Create a number of paths that can be drawn in a grid showing multiple functions.
# Create a new BezierPath as separate entity to talk to. This woe
path1 = context.newPath() 
path1.rect(0, 0, 100, 100)

context.fill((1, 0, 0))
context.


# Export the document to this PDF file.
context.saveImage('_export/BezierPaths.pdf')

