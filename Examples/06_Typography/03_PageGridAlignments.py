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
#     03_PageGridAlignments.py
#
#     Draw a words on different positions of vertical alignment, based on the
#     typographic metrics and the postion of baselines.
#
#     TODO: Make the baseline alignments work.
#

from copy import copy
from pagebot import getContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em, pt, p, upt
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import BASE_LINE_BG, BASE_INDEX_LEFT, GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG

context = getContext()

W = H = pt(1000) # Document size
PADDING = pt(100) # Page padding on all sides
G = p(2) # 2 Pica gutter
PW = W - 2*PADDING # Usable padded page width
PH = H - 2*PADDING # Usable padded page height
CW = (PW - G)/2 # Column width
CH = PH
# Hard coded grid, will be automatic in later examples.
GRIDX = ((CW, G), (CW, 0))
GRIDY = ((CH, 0),)
BASELINE = pt(18)

# Get the Font instances, so they can be queried for metrics.
font = findFont('Georgia')

# Defined styles
style = dict(font=font, fontSize=125, leading=em(1.1), textFill=0.1, hyphenation=False,
    paragraphBottomSpacing=em(0.2))
captionStyle = copy(style)
captionStyle['fontSize'] = pt(10)
captionStyle['leading'] = em(1)

# Make BabelString from multiple cascading styles
t = context.newString('Hkpx', style=style) # Start with headline
# Create a new document with 1 page. Set overall size and padding.
# FIX: Float conditions only seem to work for originTop=False
doc = Document(w=W, h=H, originTop=False, padding=PADDING,  gridX=GRIDX, gridY=GRIDY, context=context, baselineGrid=BASELINE)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
view.showBaselineGrid = [BASE_LINE_BG, BASE_INDEX_LEFT]
view.showGrid = [GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG] # Set types of grid lines to show

# Get the page
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page.
# Red frame to show position and dimensions of the text box element.
# Default behavior of the textbox is to align the text at "top of the em-square".
t = context.newString('Hkpx0\n', style=style) 
t += context.newString('Move baseline to top', style=captionStyle)
c0 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), 
    conditions=[Left2Left(), Baseline2Top()])

t = context.newString('Hkpx1\n', style=style) 
t += context.newString('Move to top and then round baseline down to grid', style=captionStyle)
c1 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), 
    conditions=[Right2Right(), Top2Top(), BaselineDown2Grid()])

t = context.newString('Hkpx2\n', style=style) 
t += context.newString('Move to half page and round baseline up to grid', style=captionStyle)
y = page.ph/2 + page.pb
c2 = newTextBox(t, y=y, parent=page, w=CW, stroke=(1, 0, 0), 
    conditions=[Left2Left(), BaselineDown2Grid()])

t = context.newString('Hkpx3\n', style=style) 
t += context.newString('Move half of page and round baseline down to grid', style=captionStyle)
y = page.ph/2 + page.pb
c3 = newTextBox(t, y=y, parent=page, w=CW, stroke=(1, 0, 0), 
    conditions=[Right2Right(), BaselineDown2Grid()])

t = context.newString('Hkpx4\n', style=style) 
t += context.newString('Move to bottom of page and round baseline up to grid', style=captionStyle)
c4 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), 
    conditions=[Left2Left(), Bottom2Bottom(), BaselineDown2Grid()])

t = context.newString('Hkpx5\n', style=style) 
t += context.newString('Move last baseline to bottom', style=captionStyle)
c5 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), 
    conditions=[Right2Right(), Baseline2Bottom(index=-1)])

# Solve the page/element conditions, so the text box as it's position and size.
doc.solve()
# Get the position of the first baseline of the text.
#print(sorted(c1.baselines))
#print(firstLine, firstLine.y)
#print(firstLine[0].fontMatrix)
"""
firstLine = c00.textLines[0]
ry = c00.getRounded2Grid(firstLine.y)
c00.y += firstLine.y - ry

firstLine = c01.textLines[0]
ry = c01.getRounded2Grid(firstLine.y, roundDown=True)
c01.y += firstLine.y - ry

firstLine = c10.textLines[0]
ry = c10.getRounded2Grid(upt(firstLine.xHeight))
print(ry, firstLine.y)
c10.y += firstLine.xHeight - upt(ry)

firstLine = c11.textLines[0]
ry = c11.getRounded2Grid(upt(firstLine.xHeight), roundDown=True)
c11.y += firstLine.xHeight - upt(ry)

newLine(y=ry, w=c00.w, h=0, stroke=(1, 0, 1), strokeWidth=3, parent=c00)
newLine(y=ry, w=c00.w, h=0, stroke=(1, 0, 1), strokeWidth=3, parent=c00)

newLine(y=firstLine.y-firstLine.xHeight, w=c00.w, h=0, stroke=(1, 0, 1), strokeWidth=1, parent=c00)
newLine(y=firstLine.y-firstLine.capHeight, w=c00.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=c00)
# FIX: Something with the ascender position? Or is it showing the max-value for all glyphs?
newLine(y=firstLine.y-firstLine.ascender, w=c00.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=c00)
newLine(y=firstLine.y-firstLine.descender, w=c00.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=c00)
"""

# Export the document to this PDF file.
doc.export('_export/PageGridAlignments.pdf')

