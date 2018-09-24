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
#     that are used by conditions.
#     Test on variations of origin alignments and top/bottom of element origin.
#
from pagebot.document import Document # Get the main Document class
from pagebot.toolbox.units import pt, inch, p
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
TP = 5*BASELINE
RP = 3*BASELINE
BP = 6*BASELINE
LP = 4*BASELINE
PADDING = TP, RP, BP, LP # Page padding related to baseline in this example.
W, H = B5
EW = W - LP - RP
EH = H - TP - BP

E_FILL = color(0.5, 0.5, 0.5, 0.5)
R = 10 # Radius of the red/green circles.

CONDS = []#[Fit()]

doc = Document(w=W, h=H, padding=PADDING, 
    autoPages=2*3, # Create multiple pages, to show page origin top/bottom and element alignments.
    baselineGrid=BASELINE, baselineGridStart=BASELINE_START)

view = doc.view # Get the current view of this document. Defaulse it PageView.
view.showPadding = True # Show the padding of the page. The size is then (page.pw, page.ph)

page = doc[1]
page.originTop = True # Origin on top of bottom should make not differenc
page.padding = PADDING
r1 = newRect(conditions=CONDS, fill=E_FILL, parent=page)
r1.showOrigin = True
# 'Origin Top, box alignment top-left', 
r1.xAlign = LEFT
r1.yAlign = TOP
#page.solve() # Make the r1 fit the page padding
r1.x = LP
r1.y = TP
r1.size = EW, EH

newCircle(x=r1.x+r1.w/2-R, y=r1.y, r=R, fill=color(rgb='green'), parent=page) # x,y position
newCircle(x=r1.center+R, y=r1.top, r=R, fill=color(rgb='red'), parent=page) # sides location
 
newCircle(x=r1.x+r1.w-R, y=r1.y+r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x+r1.w/2-R, y=r1.y+r1.h, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.bottom, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-R, y=r1.y+r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)


page = doc[2]
page.originTop = True # Origin on top of bottom should make not differenc
page.padding = PADDING
r1 = newRect(conditions=CONDS, fill=E_FILL, parent=page)
r1.showOrigin = True
# 'Origin Top, box alignment middle-center', 
r1.xAlign = CENTER
r1.yAlign = MIDDLE
#page.solve() # Make the r1 fit the page padding
r1.x = LP + EW/2
r1.y = TP + EH/2
r1.size = EW, EH

newCircle(x=r1.x-R, y=r1.y-r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.top, r=R, fill=color(rgb='red'), parent=page)
 
newCircle(x=r1.x+r1.w/2-R, y=r1.y, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-R, y=r1.y+r1.h/2, r=R, fill=color(rgb='green'), parent=page) # By coordinates
newCircle(x=r1.center+R, y=r1.bottom, r=R, fill=color(rgb='red'), parent=page) # By positioning on sides

newCircle(x=r1.x-r1.w/2-R, y=r1.y, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)


page = doc[3]
page.originTop = True # Origin on top of bottom should make not differenc
page.padding = PADDING
r1 = newRect(conditions=CONDS, fill=E_FILL, parent=page)
r1.showOrigin = True
# 'Origin Top, box alignment bottom-right', 
r1.xAlign = RIGHT
r1.yAlign = BOTTOM
#page.solve() # Make the r1 fit the page padding
r1.x = LP + EW
r1.y = TP + EH
r1.size = EW, EH

newCircle(x=r1.x-r1.w/2-R, y=r1.y-r1.h, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.top, r=R, fill=color(rgb='red'), parent=page)
 
newCircle(x=r1.x-R, y=r1.y-r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-r1.w/2-R, y=r1.y, r=R, fill=color(rgb='green'), parent=page) # By coordinates
newCircle(x=r1.center+R, y=r1.bottom, r=R, fill=color(rgb='red'), parent=page) # By positioning on sides

newCircle(x=r1.x-r1.w-R, y=r1.y-r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)


page = doc[4]
page.originTop = False # Origin on top of bottom should make not differenc
page.padding = PADDING
r1 = newRect(conditions=CONDS, fill=E_FILL, parent=page)
r1.showOrigin = True
# 'Origin Bottom, box alignment top-left', 
r1.xAlign = LEFT
r1.yAlign = TOP
#page.solve() # Make the r1 fit the page padding
r1.x = LP 
r1.y = BP + EH
r1.size = EW, EH

newCircle(x=r1.x+r1.w/2-R, y=r1.y, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.top, r=R, fill=color(rgb='red'), parent=page)
 
newCircle(x=r1.x+r1.w-R, y=r1.y-r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x+r1.w/2-R, y=r1.y-r1.h, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.bottom, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-R, y=r1.y-r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)


page = doc[5]
page.originTop = False # Origin on top of bottom should make not differenc
page.padding = PADDING
r1 = newRect(conditions=CONDS, fill=E_FILL, parent=page)
r1.showOrigin = True
# 'Origin Bottom, box alignment middle-center', 
r1.xAlign = CENTER
r1.yAlign = MIDDLE
#page.solve() # Make the r1 fit the page padding
r1.x = LP + EW/2
r1.y = BP + EH/2
r1.size = EW, EH

newCircle(x=r1.x-R, y=r1.y+r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.top, r=R, fill=color(rgb='red'), parent=page)
 
newCircle(x=r1.x+r1.w/2-R, y=r1.y, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-R, y=r1.y-r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.bottom, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-r1.w/2-R, y=r1.y, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)


page = doc[6]
page.originTop = False # Origin on top of bottom should make not differenc
page.padding = PADDING
r1 = newRect(conditions=CONDS, fill=E_FILL, parent=page)
r1.showOrigin = True
# 'Origin Bottom, box alignment bottom-right', 
r1.xAlign = RIGHT
r1.yAlign = BOTTOM
#page.solve() # Make the r1 fit the page padding
r1.x = LP + EW
r1.y = BP
r1.size = EW, EH

newCircle(x=r1.x-r1.w/2-R, y=r1.y+r1.h, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.top, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-R, y=r1.y+r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.right+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-r1.w/2-R, y=r1.y, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.center+R, y=r1.bottom, r=R, fill=color(rgb='red'), parent=page)

newCircle(x=r1.x-r1.w-R, y=r1.y+r1.h/2, r=R, fill=color(rgb='green'), parent=page)
newCircle(x=r1.left+R, y=r1.middle, r=R, fill=color(rgb='red'), parent=page)


# Export the document showing the baselines of the page as horizontal lines and the padding.  
doc.export('_export/OriginTopBottom.pdf')
