# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     Build a type specimen similar as, and tribute to, the good old Fontographer 2.5 KeyMap page.
#
from __future__ import division

from random import random
from math import sin, cos, radians

from pagebot.toolbox.units import pointOffset, inch, pt, upt
from pagebot.elements import *
from pagebot.constants import A4
from pagebot.document import Document
from pagebot.conditions import *
from pagebot.toolbox.color import color
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.contexts.platform import getContext
context = getContext()

f = findFont('Roboto-Regular')

W, H = A4
GRIDX = GRIDY = 8
PADDING = 36, 42, 60, 56
SQSIZE = inch(0.5)
SQMR = 14.5
SQMB = 46
SQML = 12

class GlyphSquare(Element):
    def build(self, view, origin, drawElements=True):
        """Draw the text on position (x, y). Draw background rectangle and/or
        frame if fill and/or stroke are defined."""
        context = view.context # Get current context
        b = context.b
        
        p = pointOffset(self.origin, origin)
        p = self._applyScale(view, p)
        px, py, _ = p = self._applyAlignment(p) # Ignore z-axis for now.

        context.stroke(self.css('stroke'), w=self.css('strokeWidth'))
        context.fill(self.css('fill'))
        context.rect(px, py, self.w, self.h)
                 
        self._restoreScale(view)

# Create a new doc, with the right amount of frames/pages.
doc = Document(w=W, h=H, originTop=False, context=context)

view = doc.view
view.showPagePadding = True

page = doc[1]
page.padding = PADDING
#newImage('gallery/Fog35KeyMap.png', parent=page, z=100, conditions=[Fit2WidthSides(), Top2TopSide()])
newRect(h=inch(1), mb=inch(0.6), parent=page, fill=0.4, conditions=[Fit2Width(), Top2Top()])
for gridX in range(GRIDX):
    for gridY in range(GRIDY):
        GlyphSquare(name='square%d-%d' % (gridX, gridY), w=SQSIZE, h=SQSIZE,
            ml=SQML, mr=SQMR, mb=SQMB,
            parent=page, fill=color(0.95, a=0.8), stroke=0, strokeWidth=0.25,
            conditions=[Right2Right(), Float2Top(), Float2Left()]
        )
doc.solve()
doc.export('_export/%s_Fog35-KeyMap.pdf' % f.info.familyName)
