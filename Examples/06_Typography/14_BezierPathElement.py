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
#     

from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color, noColor
from pagebot.toolbox.units import em, pt
from pagebot.elements.paths import PageBotPath
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import * # Import all constants for convenience

context = getContext()

W = H = 1000 # Document size
PADDING = 100 # Page padding on all sides. Select value and cmd-drag to change interactive.
CW = pt(200)
G = pt(12)

# Dummy text, used several times to create the length we need for this example
text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

font = findFont('Roboto-Regular')

# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, context=context, originTop=False)
# Get the default page view of the document and set viewing parameters
view = doc.view
# Show the usable space (=page.padding) of the page, which the same as the box after fitting
view.showPadding = True
view.showOrigin = False
view.showTextOverflowMarker = False
# Get the first (and only automatic created) page of the document
page = doc[1]

# Create a number of paths that can be drawn in a grid showing multiple functions.
# Create a new BezierPath as separate entity to talk to.
path = PageBotPath(context, style=dict(fill=color(rgb='yellow'), stroke=color(rgb='red'), strokeWidth=pt(0.5)))
path.text('B', style=dict(font=font.path, fontSize=400))
path = path.removeOverlap()

e = Paths(path, parent=page, mr=G, mb=G, fill=0.9, h=CW, conditions=[Right2Right(), Float2Top(), Float2Left()])
#e.xy = page.pl, page.pb

path = PageBotPath(context, style=dict(fill=noColor, stroke=color(0.5), strokewidth=0.5))
path.rect(0, 0, CW-G, CW-G)
path.rect(G, G, CW-G, CW-G)
path.rect(G/2, G, CW-G, CW-G)
path.rect(G, G/2, CW-G, CW-G)
path = path.removeOverlap()
e = Paths(path, parent=page, mr=G, mb=G, h=CW, conditions=[Right2Right(), Float2Top(), Float2Left()])
#e.xy = page.pl, page.pb

# Solve the page/element conditions
doc.solve()
# Export the document to this PDF file.
doc.export('_export/PageBotPaths.pdf')

