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
from pagebot.toolbox.units import pt
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.finder import Finder # 
from pagebot.publications.magazine.magazine import Magazine

context = getContext()

fontRegular = findFont('Upgrade-Regular')
fontBold = findFont('Upgrade-Bold')

coverTitleStyle = dict(font=fontBold, textFill=color(1, 0, 0), fontSize=pt(100))

# Let the Magazine create a Finder instance, where to find resources, such as images.
m = Magazine(RESOURCES_PATH, size=A4, padding=pt(40), context=context)

# Make a cover Image element with composition conditions
coverImage = m.find(pattern='pepper')[0]
coverImage.h = 500
coverImage.conditions = [Top2TopSide()]#, Fit2BottomSide()]
coverImage.conditions = [Bottom2BottomSide()]#, Fit2BottomSide()]

titleBox = newTextBox('Magazine', style=coverTitleStyle, conditions=[Left2Left(), Fit2Width(), Top2Top()])

# Create a coverFront part/element in the Magazine, including a Cover part.
# coverFront(=part)-->cover(=part)-->coverPage-->coverImage(=Image)
coverFront = m.newCoverFront() # Creates automatic Cover part by default.
coverFront.cover.append(coverImage) # Appending an element, creates a cover page.
coverFront.cover.append(titleBox)

# Compose all parts of the magazine and get the resulting Document instance.
doc = m.compose()
# Solve conditions
doc.solve() # Solve any unsolved conditions on the pages.

# Set view paramters
view = doc.view
view.showPadding = True
view.showFrame = True
view.showCropMarks = True
view.showRegistrationMarks = True
view.padding = pt(80)

print(coverImage.box)

# Export the document as PDF.
doc.export('_export/BuildOne.pdf')
