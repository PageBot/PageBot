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
#     getRectFromRange.py
#
import sys
from pagebot import getContext
context = getContext()
if not context.isDrawBot:
    print('Example only runs on DrawBot.')
    sys.exit()

import CoreText
import AppKit

from drawBot.context.baseContext import BaseContext

import re


def textSearch(self, txt, box, search, align):
    canHyphenate = True
    if isinstance(box, self._bezierPathClass):
        canHyphenate = False
        path = box._getCGPath()
        (x, y), (w, h) = CoreText.CGPathGetPathBoundingBox(path)
    else:
        x, y, w, h = box
        path = CoreText.CGPathCreateMutable()
        CoreText.CGPathAddRect(path, None, CoreText.CGRectMake(x, y, w, h))
    
    
    canDoGradients = True
    attrString = self.attributedString(txt, align=align)
    if canHyphenate and self._state.hyphenation:
        attrString = self.hyphenateAttributedString(attrString, w)
    
    txt = attrString.string()
    searchRE = re.compile(search)
    locations = []
    for found in searchRE.finditer(txt):
        locations.append((found.start(), found.end()))

    setter = CoreText.CTFramesetterCreateWithAttributedString(attrString)
    box = CoreText.CTFramesetterCreateFrame(setter, (0, 0), path, None)

    ctLines = CoreText.CTFrameGetLines(box)
    origins = CoreText.CTFrameGetLineOrigins(box, (0, len(ctLines)), None)

    
    rectangles = []
    for startLocation, endLocation in locations:
        minx = miny = maxx = maxy = None
        for i, (originX, originY) in enumerate(origins):
            ctLine = ctLines[i]
            bounds = CoreText.CTLineGetImageBounds(ctLine, None)
            if bounds.size.width == 0:
                continue
            _, ascent, descent, leading = CoreText.CTLineGetTypographicBounds(ctLine, None, None, None)
            height = ascent + descent
            lineRange = CoreText.CTLineGetStringRange(ctLine)
            miny = maxy = originY     
            if AppKit.NSLocationInRange(startLocation, lineRange):
                minx, _ = CoreText.CTLineGetOffsetForStringIndex(ctLine, startLocation, None)    
            
            if AppKit.NSLocationInRange(endLocation, lineRange):
                maxx, _ = CoreText.CTLineGetOffsetForStringIndex(ctLine, endLocation, None)        
                rectangles.append((x+minx, y+miny-descent, maxx-minx, height))
        
            if minx and maxx is None:
                rectangles.append((x+minx, y+miny-descent, bounds.size.width-minx, height))
                minx = 0
            
    return rectangles


size(300, 484)
t = FormattedString()

t.font("Times", 30)
t += "Hello world! This is"
t.font("Helvetica", 20)
t += " cool, super cool and this is also cool..."
 
b = (16, 6, 162, 292)

textBox(t, b)

results = textSearch(BaseContext(), t, b, " ", align="left")

fill(0, 1, 0, .5)
for r in results:
    rect(*r)

results = textSearch(BaseContext(), t, b, "this", align="left")
fill(1, 1, 0, .5)
for r in results:
    rect(*r)
