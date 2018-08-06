# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2017 Thom Janssen <https://github.com/thomgb>
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     040_PageGridAlignments.py
#
#     Draw a words on different positions of vertical alignment, based on the
#     typographic metrics and the postion of baselines.
#
#from pagebot.contexts.flatcontext import FlatContext
from pagebot.contexts.platform import getContext

from pagebot.fonttoolbox.objects.font import findFont
from pagebot.document import Document
from pagebot.elements import * # Import all types of page-child elements for convenience
from pagebot.toolbox.color import color
from pagebot.toolbox.units import em, pt, p
from pagebot.conditions import * # Import all conditions for convenience.
from pagebot.constants import GRID_LINE, GRID_INDEX, GRID_COL, GRID_ROW, GRID_SQR


#context = FlatContext()
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

# Get the Font instances, so they can be queried for metrics.
font = findFont('Georgia')

# Defined styles
style = dict(font=font, fontSize=125, leading=em(1.4), textFill=0.1, hyphenation=False,
    paragraphBottomSpacing=em(0.2))

# Make BabelString from multiple cascading styles
t = context.newString('Hkpx', style=style) # Start with headline
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING,  gridX=GRIDX, gridY=GRIDY, context=context)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
view.showTextBoxBaselines = True # Show baseline grid of the column lines.
view.showBaselineGrid = [GRID_LINE] #, GRID_INDEX
view.showGridBackground = [GRID_COL, GRID_ROW, GRID_SQR] # Set types of grid lines to show

# Get the page
page = doc[1]
page.style['baselineGridStart'] = page.pt
page.style['baselineGrid'] = pt(24)
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page.
# Red frame to show position and dimensions of the text box element.
# Default behavior of the textbox is to align the text at "top of the em-square".
c00 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), conditions=[Left2Left(), Top2Top()])
c01 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), conditions=[Right2Right(), Top2Top()])

c10 = newTextBox(t, parent=page, w=CW, stroke=(0, 0, 0.5), conditions=[Left2Left(), Float2Top()])
"""
c11 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), conditions=[Right2Right(), Float2Top()])
c20 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), conditions=[Left2Left(), Float2Top()])
c21 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), conditions=[Right2Right(), Float2Top()])
c30 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), conditions=[Left2Left(), Float2Top()])
c31 = newTextBox(t, parent=page, w=CW, stroke=(1, 0, 0), conditions=[Right2Right(), Float2Top()])
"""
# Solve the page/element conditions, so the text box as it's position and size.
doc.solve()
# Get the position of the first baseline of the text.
firstLine = c00.textLines[0]
#print(sorted(c1.baselines))
#print(firstLine, firstLine.y)
#print(firstLine[0].fontMatrix)
#newLine(x=0, y=c1.h-firstLine.y, w=page.pl, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
newLine(x=c00.x, y=c00.h-firstLine.y-firstLine.xHeight, w=c00.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
newLine(x=c00.x, y=c00.h-firstLine.y-firstLine.capHeight, w=c00.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
# FIX: Something with the ascender position? Or is it showing the max-value for all glyphs?
newLine(x=c00.x, y=c00.h-firstLine.y-firstLine.ascender, w=c00.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
newLine(x=c00.x, y=c00.h-firstLine.y-firstLine.descender, w=c00.w, h=0, stroke=(1, 0, 0), strokeWidth=1, parent=page)
# Export the document to this PDF file.
doc.export('_export/PageGridAlignments.pdf')

