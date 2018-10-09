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
#     testCTRunMetrics.py
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
from pagebot.toolbox.units import em

context.newPage(1000, 620)

#fontPath = u"Proforma-Bold"
fontPath1 = u"Upgrade-Regular" # See gallery
fontPath2 = u"Upgrade-Bold" # See gallery

# Test fonts without [liga] OT-feature. Just shows warning
#fontPath = u"Verdana-Bold"
#fontPath = u"Georgia-Bold"


#fontToolsFont = TTFont(fontPath)
#glyphOrder = fontToolsFont.getGlyphOrder()

def ctRunThing(fs, x, y):
    
    ly = y
    w, h = textSize(fs)
    attrString = fs.getNSObject()
    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    path = Quartz.CGPathCreateMutable()
    Quartz.CGPathAddRect(path, None, Quartz.CGRectMake(0, 0, w, h))
    ctBox = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)
    ctLines = CoreText.CTFrameGetLines(ctBox)
    
    for ctLine in ctLines:
        #print('---', ctLine)
        ctRuns = CoreText.CTLineGetGlyphRuns(ctLine)

        # loop over all runs
        for ctRun in ctRuns:
            # get all positions
            pos = CoreText.CTRunGetPositions(ctRun, (0, CoreText.CTRunGetGlyphCount(ctRun)), None)
            # get all glyphs
            glyphs = CoreText.CTRunGetGlyphs(ctRun, (0, CoreText.CTRunGetGlyphCount(ctRun)), None)
            #print(y, ly, pos)

            # enumerate over all pos
            for i, (gx, gy) in enumerate(pos):
                # draw a line
                context.stroke(0)
                context.line((x+gx, ly+gy), (x+gx, ly+gy + 100))
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
                leadingMax = CoreText.CTRunGetAttributes(ctRun)['NSParagraphStyle'].maximumLineHeight()
                leadingMin = CoreText.CTRunGetAttributes(ctRun)['NSParagraphStyle'].minimumLineHeight()
                print(leadingMax, leadingMin)

        fill(None)
        stroke(1, 0, 0)
        S = 8
        rect(x-S, ly-S, 2*S, 2*S) 

        ly -= leadingMax
                #text(glyphName, (x+gx+centerShift-tx*.5, y+gy-20))
      
style1 = dict(font=fontPath1, leading=em(1.1), fontSize=100, openTypeFeatures=dict(liga=False))
style1a = dict(font=fontPath1, leading=em(1.1), baselineShift=em(0.2), textColor=(1, 0, 0), fontSize=70, openTypeFeatures=dict(liga=False))
fs1 = context.newString('Ligature fifl', style=style1)
fs1 += context.newString(' 123', style=style1a)
fs1 += context.newString('\nand another line.', style=style1)
text(fs1.s, (100, 450)) # Using direct DrawBot text( ) here.
ctRunThing(fs1.s, 100, 450) # Draw lines at the glyph positions

fs2 = context.newString('Ligature fifl\nand another line.', 
    style=dict(font=fontPath2, leading=em(1.1), fontSize=100, openTypeFeatures=dict(liga=True)))
text(fs2.s, (100, 200)) # Using direct DrawBot text( ) here.
ctRunThing(fs2.s, 100, 200) # Draw lines at the glyph positions
 
saveImage('_gallery/testCTRunLigature.pdf')
