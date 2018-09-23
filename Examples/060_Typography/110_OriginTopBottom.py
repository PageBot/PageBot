#!/usr/bin/env python
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
#     110_OriginTopBottom.py
#
#     Test the relation between hard-coded positions (from e.x and e.w, etc.)
#     and the more abstract positions of e.top, e.right, e.bottom and e.left
#     Text on variations of origin alignments and top/bottom of element origin.
#
from pagebot.document import Document # Get the main Document class
from pagebot.toolbox.units import pt, inch
from pagebot.toolbox.color import color
from pagebot.contexts.platform import getContext
from pagebot.constants import (BASE_LINE_BG, BASE_Y_LEFT, BASE_INDEX_LEFT, B5, CENTER, MIDDLE,
    LEFT, RIGHT, TOP, BOTTOM)
from pagebot.elements import *
from pagebot.conditions import *

context = getContext() # Get the current context (e.g. DrawBotContext instance)

# Example baseline position, showing that start can be different from page side
# or top of text box.
BASELINE = pt(15)
BASELINE_START = 3.5 * BASELINE
PADDING = 5*BASELINE, 3*BASELINE, 6*BASELINE, 4*BASELINE # Page padding related to baseline in this example.

doc = Document(size=B5, padding=PADDING, 
    autoPages=2*3, # Create multiple pages, to show page origin top/bottom and element alignments.
    baselineGrid=BASELINE, baselineGridStart=BASELINE_START)

view = doc.view # Get the current view of this document. Defaulse it PageView.
view.padding = 0 # Define padding of the view, so there is space for crop marks
view.showBaselines = False #[BASE_LINE_BG, BASE_INDEX_LEFT] # Set to True to show baseline index
#view.showBaselines = [BASE_LINE_BG, BASE_Y_LEFT] # Use this line to show vertical positions
view.showPadding = True # Show the padding of the page. The size is then (page.pw, page.ph)
view.showCropMarks = False
view.showRegistrationMarks = False
view.showNameInfo = True # Show document/name/date info in view padding area.
view.showFrame = True # Show frame of the page size.

r = 10 # Radius of the red/green circles.

page = doc[1]
page.originTop = True # Origin on top of bottom should make not differenc
r1 = newRect(conditions=[Fit()], fill=(0.5, 0.5, 0.5, 0.5), parent=page)
# 'Origin Top, box alignment top-left', 
r1.showOrigin = True
page.solve() # Make the r1 fit the page padding
print('r1.top', r1.top, 'page.pt', page.pt, r1.top == page.pt)
newCircle(x=r1.x+r1.w/2-r, y=r1.y, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.x+r1.w/2+r, y=r1.top, r=r, fill=color(rgb='red'), parent=page)
 
print('r1.right', r1.right, page.pl + page.pw, page.w - page.pr, r1.right == page.pl + page.pw == page.w - page.pr)
newCircle(x=r1.x+r1.w-10, y=r1.y+r1.h/2, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+10, y=r1.y+r1.h/2, r=r, fill=color(rgb='red'), parent=page)

print('r1.bottom', r1.bottom, page.h - page.pb, r1.bottom == page.h - page.pb)
newCircle(x=r1.x+r1.w/2-10, y=r1.y+r1.h, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.x+r1.w/2+10, y=r1.bottom, r=r, fill=color(rgb='red'), parent=page)

print('r1.left', r1.left, page.pl, r1.left == page.pl)
newCircle(x=r1.x-10, y=r1.y+r1.h/2, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+10, y=r1.y+r1.h/2, r=r, fill=color(rgb='red'), parent=page)


page = doc[2]
page.originTop = True # Origin on top of bottom should make not differenc
r1 = newRect(conditions=[Fit()], fill=(0.5, 0.5, 0.5, 0.5), parent=page)
# 'Origin Top, box alignment middle-center', 
r1.showOrigin = True
r1.xAlign = LEFT
r1.yAlign = MIDDLE
page.solve() # Make the r1 fit the page padding
print('r1.top', r1.top, 'page.pt', page.pt, r1.top == page.pt)
newCircle(x=r1.x+r1.w/2-r, y=r1.y, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.x+r1.w/2+r, y=r1.top, r=r, fill=color(rgb='red'), parent=page)
 
print('r1.right', r1.right, page.pl + page.pw, page.w - page.pr, r1.right == page.pl + page.pw == page.w - page.pr)
newCircle(x=r1.x+r1.w-10, y=r1.y+r1.h/2, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+10, y=r1.y+r1.h/2, r=r, fill=color(rgb='red'), parent=page)

print('r1.bottom', r1.bottom, page.h - page.pb, r1.bottom == page.h - page.pb)
newCircle(x=r1.x+r1.w/2-10, y=r1.y+r1.h, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.x+r1.w/2+10, y=r1.bottom, r=r, fill=color(rgb='red'), parent=page)

print('r1.left', r1.left, page.pl, r1.left == page.pl)
newCircle(x=r1.x-10, y=r1.y+r1.h/2, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+10, y=r1.y+r1.h/2, r=r, fill=color(rgb='red'), parent=page)


page = doc[3]
page.originTop = True # Origin on top of bottom should make not differenc
r1 = newRect(conditions=[Fit()], fill=(0.5, 0.5, 0.5, 0.5), parent=page)
# 'Origin Top, box alignment bottom-right', 
r1.showOrigin = True
r1.xAlign =RIGHT
r1.yAlign = BOTTOM
page.solve() # Make the r1 fit the page padding
print('r1.top', r1.top, 'page.pt', page.pt, r1.top == page.pt)
newCircle(x=r1.x+r1.w/2-r, y=r1.y, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.x+r1.w/2+r, y=r1.top, r=r, fill=color(rgb='red'), parent=page)
 
print('r1.right', r1.right, page.pl + page.pw, page.w - page.pr, r1.right == page.pl + page.pw == page.w - page.pr)
newCircle(x=r1.x+r1.w-10, y=r1.y+r1.h/2, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+10, y=r1.y+r1.h/2, r=r, fill=color(rgb='red'), parent=page)

print('r1.bottom', r1.bottom, page.h - page.pb, r1.bottom == page.h - page.pb)
newCircle(x=r1.x+r1.w/2-10, y=r1.y+r1.h, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.x+r1.w/2+10, y=r1.bottom, r=r, fill=color(rgb='red'), parent=page)

print('r1.left', r1.left, page.pl, r1.left == page.pl)
newCircle(x=r1.x-10, y=r1.y+r1.h/2, r=r, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+10, y=r1.y+r1.h/2, r=r, fill=color(rgb='red'), parent=page)


# Export the document showing the baselines of the page as horizontal lines and the padding.  
doc.export('_export/OriginTopBottom.pdf')
