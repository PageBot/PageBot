#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testCTRunLigature.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

import CoreText
import Quartz

from fontTools.ttLib import TTFont

context.newPage(1000, 500)

#fontPath = u"Proforma-Bold"
fontPath = u"Upgrade-Bold" # See gallery

# Test fonts without [liga] OT-feature. Just shows warning
#fontPath = u"Verdana-Bold"
#fontPath = u"Georgia-Bold"


#fontToolsFont = TTFont(fontPath)
#glyphOrder = fontToolsFont.getGlyphOrder()

def ctRunThing(fs, xy):
    x, y = xy
    w, h = textSize(fs)
    box = 0, 0, w, h
    attrString = fs.getNSObject()
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    path = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(*box))
    ctBox = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    ctLines = CoreText.CTFrameGetLines(ctBox)
    ctRuns = CoreText.CTLineGetGlyphRuns(ctLines[0])

    # loop over all runs
    for run in ctRuns:
        # get all positions
        pos = CoreText.CTRunGetPositions(run, (0, CoreText.CTRunGetGlyphCount(run)), None)
        # get all glyphs
        glyphs = CoreText.CTRunGetGlyphs(run, (0, CoreText.CTRunGetGlyphCount(run)), None)
        #print(pos)

        # enumerate over all pos
        for i, (gx, gy) in enumerate(pos):
            # draw a line
            context.stroke(0)
            context.line((x+gx, y+gy), (x+gx, y+gy + 100))
            context.stroke(None)
            # get the glyph name from the glyph order
            #glyphName = glyphOrder[glyphs[i]]
            # get the shift to center the name of the glyph
            centerShift = 0
            if i < len(pos)-1:
                centerShift = (pos[i+1][0] - gx)
            else:
                # last one
                centerShift = w - gx
            centerShift *= .5
            #tx, _ = textSize(glyphName)

            #text(glyphName, (x+gx+centerShift-tx*.5, y+gy-20))
            
fs1 = context.newString('Ligature fifl', style=dict(font=fontPath, fontSize=100, openTypeFeatures=dict(liga=False)))
text(fs1.s, (100, 300)) # Using direct DrawBot text( ) here.
ctRunThing(fs1.s, (100, 300)) # Draw lines at the glyph positions

fs2 = FormattedString('Ligature fifl', font=fontPath, fontSize=100, openTypeFeatures=dict(liga=True))
text(fs2, (100, 100)) # Using direct DrawBot text( ) here.
ctRunThing(fs2, (100, 100)) # Draw lines at the glyph positions
 
saveImage('_gallery/testCTRunLigature.pdf')
