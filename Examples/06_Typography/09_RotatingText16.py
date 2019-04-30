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
#     09_RotatingText16.py
#
#     Draw a two columns with a single text, showing overflow from one column
#     into the other. Use some view.showGrid options to show the grid.
#     Use view.showBaselineGrid = True to show the default baselines of the text.

from pagebot import getContext

from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em, p, pt
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import *

context = getContext() # Probably DrawBotContext, when running in DrawBot.

W = H = pt(1000) # Document size for square pages.
PADDING = pt(100) # Page padding on all sides
G = p(2) # 2 Pica gutter
PW = W - 2*PADDING # Usable padded page width
PH = H - 2*PADDING # Usable padded page height
CW = (PW - 3*G)/4 # Column width
CH = (PH - 3*G)/4 # Column height, same as with in this example, because page is square.
# Hard coded grid, will be automatic in later examples.
GRIDX = ((CW, G), (CW, G), (CW, G), (CW, G))
GRIDY = ((CH, G), (CH, G), (CH, G), (CH, G))

text = """Considering the fact that the application allows individuals to call a phone number and leave a voice mail, which is automatically translated into a tweet with a hashtag from the country of origin. """

font = findFont('Roboto-Regular')

style = dict(font=font, fontSize=12, leading=em(1.4), textFill=0.3, hyphenation=True)
# Make long text to force box overflow
t = context.newString(text * 30, style=style)
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY, context=context, originTop=True)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
# Set types of grid lines to show on foreground/background
view.showGrid = [GRID_COL, GRID_ROW_BG, GRID_SQR_BG]
view.showBaselineGrid = False # Show default setting of baseline grid of the column lines.
#view.padding = inch(1)
#view.showFrame = True
#view.showCropMarks = True
#view.showColorBars = True

# Get the page
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page and the condition that checks on text overflow.
n = 0
for ix in range(4): # Horizontal index for x-position
    for iy in range(4): # Vertical index for y-position
        newTextBox(t, x=page.pl+ix*(CW+G), y=page.pt+iy*(CH+G), w=CW, h=CH, 
            rx=CW/2, ry=CH/2, angle=90*n/15, # Local rotation center and contructed angle.
            conditions=[Overflow2Next()], # Just overflow conditions, position is hard-coded.
            name='c%d' % n, parent=page, nextElement='c%d' % (n+1),
            showOrigin=True, # Show origin cross-hair at top-left of un-rotate text box.
            # Set the baseline flag. Note that the baseline and index rotate nicely.
            showBaselineGrid=(BASE_LINE, BASE_INDEX_RIGHT)) # Overwrite the view setting.
        t = '' # Just text in the first textbox, to it will flow into the others.
        n += 1 # Next counter that controls the textbox name and rotation angle.
doc.solve() # Solve the overflowing conditions.

# Export the document to this PDF file.
doc.export('_export/RotatingText16.pdf')

