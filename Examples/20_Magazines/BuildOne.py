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
#     BuildOne.py
#
#     Build a magazine from resources and a single MarkDown file.
#     This example script shows how to create top-down complex document
#     by a series of high-level composition instructions.
#
import os
from pagebot.contexts import getContext
from pagebot.paths import *
from pagebot.constants import * # Containing page sizes and other contants.
from pagebot.conditions import *
from pagebot.elements import *
from pagebot.toolbox.color import whiteColor, color
from pagebot.toolbox.units import pt, p
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.finder import Finder # 
from pagebot.publications.magazine.magazine import Magazine

W, H = A4Rounded

BLEED_RIGHT = p(1, 1, 1, 0)
BLEED_LEFT = p(1, 0, 1, 1)

PADDING = PT, PR, PB, PL = pt(40, 30, 30, 50)
G = pt(12)
COLUMNS = 4
CW = (W - PL - PR - G)/COLUMNS - G
CW2 = CW + G + CW
CW3 = CW2 + G + CW
CW4 = CW3 + G + CW

GH = pt(1)
COLUMNS = 4
RH = ()
GRID_X = ((CW, G), (CW, G), (CW, G), (CW, 0))

context = getContext()

fontRegular = findFont('Upgrade-Regular')
fontBold = findFont('Upgrade-Bold')

coverTitleStyle = dict(font=fontBold, textFill=color(1, 0, 0), fontSize=pt(100))

# Let the Magazine create a Finder instance, where to find resources, such as images.
m = Magazine(RESOURCES_PATH, size=(W, H), padding=PADDING, originTop=False, 
        gridX=GRID_X, gridY=GRID_X, context=context)

doc = m.newDocument(autoPages=1)

# Make a cover Image element with composition conditions
coverImage = m.find(pattern='pepper')[0]
coverImage.yAlign = BOTTOM
coverImage.h = 300
coverImage.clipPath = newRectPath(context, 100, 200)
#coverImage.conditions = [Top2TopBleed(), Fit2BottomBleed()]
coverImage.conditions = [Bottom2BottomBleed()]#, Fit2TopBleed()]

"""
#titleBox = newTextBox('Magazine', style=coverTitleStyle, fill=(1, 1, 0), conditions=[Fit2Width(), Bottom2Bottom()])
#test = newRect(fill=(1, 1, 0, 0.5), stroke=None, h=p(2), conditions=[Fit2Width(), Bottom2BottomBleed()])

# Create a coverFront part/element in the Magazine, including a Cover part.
# coverFront(=part)-->cover(=part)-->coverPage-->coverImage(=Image)
coverFront = m.newCoverFront() # Creates automatic Cover part by default.
cover = coverFront.cover.pages[0]
cover.bleed = BLEED_RIGHT
#cover.append(coverImage) # Appending an element, creates first cover Page instance.
#cover.append(titleBox)
#cover.append(test)

# Compose all parts of the magazine and get the resulting Document instance.
doc = m.compose()
# Solve conditions
doc.solve() # Solve any unsolved conditions on the pages.

# Set view paramters for the output document.
view = doc.view
view.setShowings(VIEW_PRINT, VIEW_DEBUG, VIEW_DEBUG2)
#view.showColorBars = True # Modify showing set by individual flag.

#print(coverImage.box)

print(coverImage.x, coverImage.y, coverImage.w, coverImage.h)
coverImage.h = cover.h
coverImage.bottom = 0
print(coverImage.x, coverImage.y, coverImage.w, coverImage.h)
"""

# Export the document as PDF.
doc.export('_export/BuildOne.pdf')
