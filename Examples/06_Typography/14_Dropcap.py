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
#     00_Dropcap.py
#
#     Draw one column that fills the entire usable space of the page,
#     add a positioned element, containing a dropcap and fill the rest
#     of the column as path, constructed from the position of the
#     child elements in the textbox element.
#     The usable area of the page is defined by the remainder of page.padding.

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
style = dict(font=font, fontSize=24, leading=em(1.4), textFill=0.3)
bs1 = context.newString(text[1:] + text * 10, style=style)

# Make the BabelString of the dropcap, taking the first character of t.
dropCapStyle = dict(font='Georgia', fontSize=pt(200), textFill=(1, 0, 0))
bs2 = context.newString(text[0], style=dropCapStyle)

# Create a new BezierPath object, that contains a rectangle with the size of the text box.
bpo1 = context.newPath()
bpo1.text(bs2.s)
minX, minY, maxX, maxY = path1.bounds() # Get the bounds of the dropcap pixels
dcw = maxX - minX
dch = maxY - minY
#path1.rect(page.pl, page.pb, page.pw, page.ph)

# Create another path with the size amd position of the dropcap reserved space.
# Normally this would come from the position of a child element inside the main textbox.
path2 = context.newPath()
M = 16
path2.rect(page.pl, page.pb+page.ph+dcy-dch-M, dcw-dcx+2*M, dch-dcy+2*M)
path = path1.difference(path2)
newTextBox(bs1, parent=page, yAlign=TOP, showFrame=True, conditions=[Fit()], clipPath=path)

newImage(bs2, parent=page, conditions=(Left2Left(), Top2TopSide()), w=dcw+2, h=dch*2+M)

# Solve the page/element conditions
doc.solve()
# Export the document to this PDF file.
doc.export('_export/DropcapBasics.pdf')

