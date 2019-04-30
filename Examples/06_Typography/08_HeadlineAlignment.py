# -*- coding: UTF-8 -*-
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
#     08-HeadlineAlignment.py
#
from pagebot.contexts.drawbotcontext import DrawBotContext
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.toolbox.units import em, p, pt
from pagebot.constants import *
from pagebot.elements import *
from pagebot.conditions import *
from pagebot.document import Document

context = DrawBotContext()

W, H = pt(1500, 1000) # Document size
PADDING = pt(100) # Page padding on all sides
G = p(2) # 2 Pica gutter
PW = W - 2*PADDING # Usable padded page width
PH = H - 2*PADDING # Usable padded page height
CW = (PW - G)/3 # Column width
CH = PH
# Hard coded grid for 3 columns, will be automatic in later examples.
GRIDX = ((CW, G), (CW, G), (CW, G))
GRIDY = ((CH, 0),) # No division in vertical grid.
BASELINE = G

NUM_PAGES = 1

# Get the font object, from te Roboto file that is included in PageBot resources for testing.
f = findFont('PageBot-Regular')

# Make the style dictionary for the body text.
style = dict(font=f, fontSize=24, leading=em(1.4), textFill=0.3, hyphenation=LANGUAGE_EN)
# Create a new document with 1 page. Set overall size and padding.
# TODO: View grid drawing, etc. does not work properly for originTop=True
doc = Document(w=W, h=H, padding=PADDING, gridX=GRIDX, gridY=GRIDY, context=context, 
    autoPages=NUM_PAGES, originTop=False, baselineGrid=BASELINE)
# Get the default page view of the document and set viewing parameters
view = doc.view
view.showTextOverflowMarker = True # Shows as [+] marker on bottom-right of page.
# TODO: Fix the Arrow-connection drawing
view.showFlowConnections = False # Draw arrows between elements of there is a flow.
view.showOrigin = True # Show position of elements as cross-hair
view.showGrid = [GRID_COL_BG, GRID_ROW_BG, GRID_SQR_BG] # Set types of grid lines to show for background
view.showBaselineGrid = True # Show default baseline grid of the column lines.

page = doc[1]

bs = context.newString('Headline Kphx', style=dict(font=f, fontSize=150, textFill=(1, 0, 0)))
e = newTextBox(bs, x=100, y=300, parent=page, 
	conditions=[Fit2Width(), Shrink2TextHeight(), CapHeight2Top()])
print(sorted(e.baselines), e.parent.top, e.top, e.bottom, e.bs.size, context.b.textSize(e.bs.s))
page.solve()
print(sorted(e.baselines), e.parent.top, e.top, e.bottom, e.bs.size, context.b.textSize(e.bs.s))
print(e.textLines)
doc.export('_export/HeadlineAlignment.pdf')