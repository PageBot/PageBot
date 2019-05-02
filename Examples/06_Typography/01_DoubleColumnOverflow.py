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
#     01_DoubleColumnOverflow.py
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
from pagebot.mining.filibuster.samplecontent import SampleContent

sampleContent = SampleContent()
# Uncomment to show the attribute names of
# available sample content.
#print(sampleContent.info)
# Dummy text
text = ' '.join(sampleContent.articles[:3])

context = getContext()

W = H = pt(1000) # Document size
PADDING = pt(100) # Page padding on all sides
G = p(2) # 2 Pica gutter
PW = W - 2*PADDING # Usable padded page width
PH = H - 2*PADDING # Usable padded page height
CW = (PW - G)/2 # Column width
CH = PH
# Hard coded grid, will be automatic in later examples.
GRIDX = ((CW, G), (CW, G))
GRIDY = ((CH, 0),)

font = findFont('PageBot-Regular')

style = dict(font=font, fontSize=24, leading=em(1.4), textFill=0.3, hyphenation=True)
# Make long text to force box overflow
t = context.newString(text, style=style)
# Create a new document with 1 page. Set overall size and padding.
doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY, context=context, originTop=True)
# Get the default page view of the document and set viewing parameters
view = doc.view
# Set types of grid lines to show on foreground/background
view.showGrid = [GRID_COL, GRID_ROW_BG, GRID_SQR_BG]
view.showBaselineGrid = False # Show default setting of baseline grid of the column lines.

# Get the page
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page and the condition that checks on text overflow.
c1 = newTextBox(t, w=CW, name='c1', parent=page, 
    showOrigin=True, nextElement='c2',
    conditions=[Left2Left(), Top2Top(), Fit2Height(), Overflow2Next()])
# Text without initial content, will be filled by overflow of c1.
# Not showing the [+] marker, as the overflow text fits in the second column.
c2 = newTextBox(w=CW, name='c2', parent=page, 
    showOrigin=True, 
    showBaselineGrid=(BASE_LINE, BASE_INDEX_LEFT, BASE_Y_RIGHT), # Overwrited view setting.
    conditions=[Right2Right(), Top2Top(), Fit2Height()])

# Solve the page/element conditions
doc.solve()

# Export the document to this PDF file.
doc.export('_export/DoubleColumnOverflow.pdf')

