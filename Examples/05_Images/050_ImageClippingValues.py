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
#     050_ImageClippingValues.py
#
#     Draw a number of images on a page to show the influence of parameters.
#
from pagebot import getContext

from pagebot import getResourcesPath
from pagebot.document import Document
from pagebot.toolbox.color import color, noColor
from pagebot.toolbox.units import em, p, pt, inch, degrees
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import *
from pagebot.elements import newTextBox
from pagebot.elements.pbimage2 import Image

#context = FlatContext()
context = getContext()

# Example image that has nice areas to put text as example.
imagePath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'

W = H = pt(1000) # Document size
PADDING = pt(100) # Page padding on all sides
IH = PADDING
G = pt(12)

# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, context=context, originTop=False)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showPadding = True
view.showOrigin = False
view.padding = 40
view.showCropMarks = True
view.showFrame = True
# Get the page
page = doc[1]
page.padding = PADDING


if 1: 
    # Make image box as child element of the page and set its layout conditions.
    im = Image(imagePath, h=IH, w=IH, fill=(1, 0, 0, 0.5), parent=page, 
        conditions=[Right2Right(), Float2Top(), Float2Left()], mr=G, mb=G)
    style1 = dict(fontSize=14, textFill=0, xTextAlign=CENTER)
    bs = context.newString('1', style=style1)
    newTextBox(bs, parent=im, w=IH, fill=noColor,
        conditions=(Center2Center(), Middle2Middle()))

if 1:
    # Make image box as child element of the page and set its layout conditions.
    im = Image(imagePath, h=IH, w=IH, fill=(1, 1, 0, 0.5), parent=page, 
        conditions=[Right2Right(), Float2Top(), Float2Left()], mr=G, mb=G)
    style2 = dict(fontSize=14, textFill=0, xTextAlign=CENTER)
    bs = context.newString('2', style=style2)
    newTextBox(bs, parent=im, w=IH, fill=noColor,
        conditions=(Center2Center(), Middle2Middle()))

if 1:
    # Make image box as child element of the page and set its layout conditions.
    im = Image(imagePath, h=IH, w=IH, fill=(1, 0, 1, 0.5), parent=page, 
        conditions=[Right2Right(), Float2Top(), Float2Left()], mr=G, mb=G)
    bs = context.newString('3', style=dict(fontSize=14, textFill=0, xTextAlign=CENTER))
    newTextBox(bs, parent=im, w=IH, fill=noColor,
        conditions=(Center2Center(), Middle2Middle()))

# Solve the page/element conditions
doc.solve()

# Export the document to this PDF file.
doc.export('_export/ImageClippingValues.pdf')

