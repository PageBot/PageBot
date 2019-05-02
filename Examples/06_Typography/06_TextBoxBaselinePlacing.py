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
#     06_TextBoxBaselinePlacing.py
#
#     Draw a two columns with a single text, showing overflow from one column
#     into the other. Use some view.showGrid options to show the grid.
#     Use view.showBaselineGrid = True to show the default baselines of the text.
#     Then use BASE_TOP and BASE_BOTTOM to place the top and bottom baseline
#     on vertical position page.h/2

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

# Dummy text, combining some articles to create the length we need for this example
text = ' '.join(sampleContent.articles[:2])

font = findFont('PageBot-Regular')
print(font)

style = dict(font=font, fontSize=24, leading=em(1.4), textFill=0.3, hyphenation=True)
# Make long text to force box overflow
t = context.newString(text, style=style)
# Create a new document with 1 page. Set overall size and padding.
# TODO: View drawing for OriginTop=True does not work properly 
doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY, context=context, originTop=False)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
# Set types of grid lines to show on foreground/background
view.showGrid = [GRID_COL, GRID_ROW_BG, GRID_SQR_BG]
view.showBaselineGrid = False # Show default setting of baseline grid of the column lines.

# Get the page
page = doc[1]
# Make text box as child element of the page and set its layout conditions
# to fit the padding of the page and the condition that checks on text overflow.
c1 = newTextBox(t, w=CW, h=CH, y=page.h/2, name='c1', parent=page, nextElement='c2', 
    yAlign=BASE_TOP, showOrigin=True, 
    showBaselineGrid=(BASE_LINE, BASE_INDEX_LEFT, BASE_Y_RIGHT), # Overwrite view setting.
    conditions=[Left2Left(), Bottom2Bottom(), Baseline2Grid(), Overflow2Next()])
# Text without initial content, will be filled by overflow of c1.
# Not showing the [+] marker, as the overflow text fits in the second column.
c2 = newTextBox(w=CW, h=CH, y=page.h/2, name='c2', parent=page, 
    yAlign=BASE_TOP, showOrigin=True, 
    showBaselineGrid=(BASE_LINE, BASE_INDEX_LEFT, BASE_Y_RIGHT), # Overwrite view setting.
    conditions=[Right2Right(), Bottom2Bottom(), Baseline2Grid()])

newLine(x=page.pl, y=page.h/2, w=page.pw, h=0, parent=page, stroke=(1, 0, 0))

# Solve the page/element conditions
page.solve()

# Export the document to this PDF file.
doc.export('_export/TextBoxBaselinePlacing.pdf')

