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
#     050_ImageClipping.py
#
#     Draw images with clipping paths and rotation.
#
from random import random
#from pagebot.contexts.flatcontext import FlatContext
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

# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, context=context, originTop=True)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.padding = inch(1)
view.showFrame = True
view.showPadding = True
view.showColorBars = False
view.showCropMarks = True
view.showRegistrationMarks = True

# Get the page
page = doc[1]
# Make image box as child element of the page and set its layout conditions.
im = Image(imagePath, parent=page, conditions=[Fit()], 
    showPadding=True, padding=100, stroke=(1, 0, 0))

# Rotate the whole by selecting the value and then cmd-drag to alter the value
# The elements rotate independently. Note that the image is rotating in the 
# reversed direction, so it stays upright in the clipping rectangle.
a = degrees(100)

im.angle =a 
im.fill = (0, 0, 0.7+random()*0.3)
imd = im.imageData
imd.x = 366
imd.y = 150
imd.w = 300
imd.h = 400
imd.rx = 50
imd.ry = 60
imd.angle = -a

bs = context.newString('Rotating images', style=dict(fontSize=32, textFill=1))
tb = newTextBox(bs, w=400, parent=im, conditions=(Center2Center(), Middle2Middle()), angle=-a, fill=noColor)
# Solve the page/element conditions
doc.solve()

im.rx = im.w/2
im.ry = im.h/2
# Export the document to this PDF file.
doc.export('_export/ImageClipping.pdf')

