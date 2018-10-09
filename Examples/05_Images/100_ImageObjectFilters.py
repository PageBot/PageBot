#!/usr/bin/env python3
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
#     UseImageObjectFilters.py
#
#     This script generates page that show the behavior and working of the DrawBot
#     ImageObject filters.
#

from pagebot import getResourcesPath
from pagebot.fonttoolbox.objects.family import getFamily
from pagebot.constants import TOP, BOTTOM, A4
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.document import Document
from pagebot.toolbox.color import color
# Document is the main instance holding all information about the
# document together (pages, styles, etc.)

W, H = A4

IMAGE_PATH = getResourcesPath() + '/images/peppertom_lowres_398x530.png'

family = getFamily('Roboto')
font = family.findFont(weight=400)
fontItalic = family.findFont(weight=400, italic=True)

GUTTER = 8 # Distance between the squares.
SQUARE = 10 * GUTTER # Size of the squares
CW = 170
M = (W - 3*CW)/2
PADDING = M, M, M, M

FILTER_TYPES = {
}

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH = '_export/UseImageObjectFilters.pdf'

def makeDocument():

    gridX = ((CW, GUTTER), (CW, GUTTER), (CW, 0))
    doc = Document(w=W, h=H, originTop=False, title='Color Squares', autoPages=1, gridX=gridX)

    view = doc.getView()
    view.padding = 0 # Avoid showing of crop marks, etc.
    view.showOrigin = False
    view.showGrid = True

    # The current view holds the context
    context = view.context

    # Get list of pages with equal y, then equal x.
    #page = doc[1[0] # Get the single page from te document.
    page = doc[1] # Get page on pageNumber, first in row (this is only one now).
    page.name = 'This is a demo page for floating child elements'
    page.padding = PADDING

    group = newGroup(parent=page, conditions=[Fit()])
    group.solve()

    for n in range(15):
        img = newImage(path=IMAGE_PATH, x=50,y=50, z=10, padding=0, mb=GUTTER,
                       parent=group, w=CW-2, h=CW-2, #clipRect=(120, 120, 1440, 440),
                       conditions=(Right2Right(),
                                   Float2Top(),
                                   Float2Left(),
                                   SolveBlock(),
                                   #Shrink2BlockBottom()
                                   ),
                       yAlign=BOTTOM,
                       #fill=color(0, 1, 0, 0.3),
                       #stroke=color(1, 0, 0)
                       )

        filters = [
            #('colorClamp', ((1, 0, 0, 0.5), (0.5, 0, 0, 0.5))),

            # colorControls(saturation=None, brightness=None, contrast=None)
            # Adjusts saturation, brightness, and contrast values.
            # Attributes: saturation a float, brightness a float, contrast a float.
            #('colorControls', (0.2, 0, 1)),

            # gammaAdjust(power=None)
            # Adjusts midtone brightness.
            # Attributes: power a float.
            #('gammaAdjust', (10,)),

            # hueAdjust(angle=None)
            # Changes the overall hue, or tint, of the source pixels.
            # Attributes: angle a float in degrees.
            #('hueAdjust', (80.2,)),

            # temperatureAndTint(neutral=None, targetNeutral=None)
            # Adapts the reference white point for an image.
            # Attributes: neutral a tuple, targetNeutral a tuple.
            #('temperatureAndTint', ((1, 1, 1), (0.1, 0.1, 0.5))),

            # whitePointAdjust(color=None)
            # Adjusts the reference white point for an image and maps all colors in the source using the new reference.
            # Attributes: color RGBA tuple Color (r, g, b, a).
            #('whitePointAdjust', ((1, 0.45, 1, 1),)),

            # colorInvert()
            # Inverts the colors in an image.
            ('colorInvert', {}),

            #('colorPosterize', (2,))

            # sepiaTone(intensity=None)
            # Maps the colors of an image to various shades of brown.
            # Attributes: intensity a float.
            #('sepiaTone', (0.4,)),

            #droste(insetPoint0=None, insetPoint1=None, strands=None, periodicity=None, rotation=None, zoom=None)
            #('droste', ((0.3, 0.4), (0.8, 0.8), 0.4, 0.6, 0.7, 0.1)),

            # twirlDistortion(center=None, radius=None, angle=None)
            # Rotates pixels around a point to give a twirling effect.
            # Attributes: center a tuple (x, y), radius a float, angle a float in degrees.
            #('twirlDistortion', ((150, 150), 200, 0.4)),
        ]
        img.addFilter(filters)
        # Give parent on creation, to have the css chain working.

        # Caption falls through the yr2 (with differnt z) and lands on yr1 by Float2BottomSide()
        captionStyle = dict(font=font.path, fontSize=11, textFill=color(0))
        captionConditions = (Fit2Width(), Float2Top())
        fs = context.newString('Captions float below the image', style=captionStyle)
        img.caption = newTextBox(fs, name='Caption', z=0, conditions=captionConditions,
            padding=4, yAlign=TOP,
                #strokeWidth=0.5,
                #fill=color(0, 0, 1, 0.3),
                #stroke=color(0, 0, 1),
            )

    score = page.solve()
    if score.fails:
        print(score.fails)

    #print(img.h)
    #for e in img.elements:
    #    print(e.h)

    return doc # Answer the doc for further doing.

d = makeDocument()
d.export(EXPORT_PATH)

