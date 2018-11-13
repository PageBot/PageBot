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
#     14_Dropcap.py
#
#     Draw one column that fills the entire usable space of the page,
#     add a positioned element, containing a dropcap and fill the rest
#     of the column as path, constructed from the position of the
#     child elements in the textbox element.
#     The usable area of the page is defined by the remainder of page.padding.
#
#     TODO: This example needs to be more generalized, hiding most of the code.
#
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import * # Import all constants for convenience

context = getContext()

W = H = 1000 # Document size
PADDING = 100 # Page padding on all sides. Select value and cmd-drag to change interactive.

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

# Show the principle of building a dropcap.
# In normal PageBot usage, this is hidden as child elements of TextBox that define the layout
# of the clipping path. Here is it shown as separate steps.

# Make main text, skipping the first character
style = dict(font=font, fontSize=24, leading=em(1.4))
bs1 = context.newString(text[1:] + text * 10, style=style)

# Make the BabelString of the dropcap, taking the first character of t.
dropCapStyle = dict(font='Georgia-Bold', fontSize=pt(250))

PADDING = pt(12)

# Create a new BezierPath object, that contains a rectangle with the size of the text box.
dropCapPath = PageBotPath(context=context)
dropCapPath.text(text[0], style=dropCapStyle) # Place the initial letter as drop cap. Path size is calculated around the result.
minX, minY, maxX, maxY = dropCapPath.bounds() # Get the bounds of the dropcap pixels
dcw = maxX - minX
dch = maxY - minY
dropCapPathFrame = PageBotPath(context=context)
dropCapPathFrame.rect(0, 0, maxX+PADDING, maxY+PADDING)
dropCapPathFrame.moveBy((0, page.ph - dch - PADDING))

# Create another path with the size and position of the dropcap reserved space.
# Normally this would come from the position of a child element inside the main textbox.
# Note that the core context.newPath() answers a DrawBot.BezierPath, which is contained
# by a PageBothPath() instance.
textFramePath = PageBotPath(context=context)
textFramePath.rect(0, 0, page.pw, page.ph) # Make a rectangle path with size of text box.
# Make a new path for the available text flow, which is the difference between the paths
textFlowPath = textFramePath.difference(dropCapPathFrame)
newTextBox(bs1, parent=page, yAlign=TOP, showFrame=True, conditions=[Fit()], clipPath=textFlowPath)

newPaths(textFlowPath, parent=page, conditions=(Left2Left(), Top2Top()))
newPaths(dropCapPath, parent=page, mr=PADDING, mb=PADDING, fill=(1, 0, 0), conditions=(Left2Left(), Top2Top()))

# Solve the page/element conditions
doc.solve()
# Export the document to this PDF file.
doc.export('_export/DropcapBasics.pdf')

