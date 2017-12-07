#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     fitVariableHeadline.py
#
#     Demo version of pagebot.fonttoolbox.variablefontbuilder.fitVariableWidth,
#     to show usage and format of the answered dictionary.
#     For real use, import the function as:
#     from pagebot.fonttoolbox.variablefontbuilder import fitVariableWidth
#
import copy
from pagebot import getRootPath
from pagebot.fonttoolbox.objects.font import Font, getFontByName
from pagebot.fonttoolbox.variablefontbuilder import (getVariableFont,
                                                     fitVariableWidth)

ROOT_PATH = getRootPath()
FONT_PATH = ROOT_PATH + '/Fonts/fontbureau/AmstelvarAlpha-VF.ttf'
f = Font(FONT_PATH,
         install=True) # Get PageBot Font instance of Variable font.

HEADLINE_SIZE = 36
HEADLINE = """When fonts started a new world."""


MIN_WDTH = 0 # Minimum value of width [wdth] axis. 0 == Normal width
MAX_WDTH = 0.6 # Maximum amount of compressions. Larger value gives
               # more condensed instance of the Variable Font.
assert MIN_WDTH < MAX_WDTH

# Amount of condensed-ness > 0
condensedLocation = dict(opsz=HEADLINE_SIZE, wdth=MAX_WDTH, wght=0.7)

# Full default width = 0
wideLocation = dict(opsz=HEADLINE_SIZE, wdth=MIN_WDTH, wght=0.7)

W = 630
H = 500
Width = 200
PADDING = 20
M = 30

INTERACTIVE = False # Interactive or save as animation.
FRAMES = 60

LINE_ENDINGS = []
for n in range(20):
    LINE_ENDINGS.append(int(random()*20))

# Drawn torn-off page top
PAGE_FRAME = None
 
def drawPageFrame(w):
    fill(1)
    stroke(0)
    path = BezierPath()
    path.moveTo((PADDING, H-PADDING))
    path.lineTo((PADDING+w, H-PADDING))
    path.lineTo((PADDING+w, H/2+PADDING))
    path.curveTo((PADDING+w/2, H/2+PADDING),
                 (PADDING+w/2, H/2+PADDING-M/2),
                 (PADDING, H/2+PADDING-M/2))
    path.closePath()
    drawPath(path)
    fill(None)
    stroke(0.5)
    strokeWidth(4)
    leading = 14
    for n in range(10):
        line((PADDING+M, H-5*PADDING-n*leading),
             (PADDING+w-M-LINE_ENDINGS[n], H-5*PADDING-n*leading))
    
def draw(w, y, drawVariable):
    u"""
      Draw 3 lines of text: the boundaries of with the width axis and
      the interpolated width from the slider value.
      If the slider goes of the extremes, then the middle line
      stops at the boundary width.
    """
    d = fitVariableWidth(f, HEADLINE, w, HEADLINE_SIZE,
                         condensedLocation, wideLocation)
    # move the canvas
    save()
    if not drawVariable:
        translate(0, -H/2+PADDING/2)
    drawPageFrame(d['width']+2*M)
    restore()
    
    minWidth = d['condensedWidth']
    maxWidth = d['wideWidth']
    fixedWidth = minWidth + (maxWidth - minWidth)/2
    dFixed = fitVariableWidth(f, HEADLINE, fixedWidth, HEADLINE_SIZE,
                              condensedLocation, wideLocation)

    if drawVariable:
        text(d['fs'], (PADDING+M, y-PADDING-M))
    else:
        # Draw the instance choice of 3
        if w < fixedWidth:
            text(d['condensedFs'], (PADDING+M, y-PADDING-M))
        elif w < maxWidth:
            text(dFixed['fs'], (PADDING+M, y-PADDING-M))
        else:
            text(d['wideFs'], (PADDING+M, y-PADDING-M))
    
if INTERACTIVE:
    Variable([
        #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
        dict(name='Width',
             ui='Slider',
             args=dict(minValue=PADDING,
                       value=200,
                       maxValue=W-2*PADDING))
    ], globals())

    draw(Width)
else:
    pageFrame = None
    angle = 0
    while angle < 360:
        newPage(W, H)
        fill(0.8)
        rect(0, 0, W, H)
        dx = sin(radians(angle))*0.5+0.5
        w = W/2 + (W-2*PADDING-W/2) * dx
        draw(w, H-PADDING, True)
        draw(w, (H-PADDING)/2, False)
        angle += 360/FRAMES
    saveImage('_export/fitVariableColumns.gif')

