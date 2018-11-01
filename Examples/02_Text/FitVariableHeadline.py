#!/usr/bin/env python3
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
#     fitVariableHeadline.py
#
#     Demo version of
#       pagebot.fonttoolbox.variablefontbuilder.fitVariableWidth
#     to show usage and format of the answered dictionary.
#
#     For real use, import the function as:
#     from pagebot.fonttoolbox.variablefontbuilder import fitVariableWidth
#
import copy
from math import sin, radians
from pagebot import getContext
from pagebot.fonttoolbox.fontpaths import getTestFontsPath
from pagebot.fonttoolbox.objects.font import findFont
from pagebot.fonttoolbox.variablefontbuilder import getVarFontInstance
from pagebot.toolbox.color import blackColor

context = getContext()

#f = findFont('Amstelvar-Roman-VF') # Get PageBot Font instance of Variable font.
#f = findFont('AmstelvarAlpha-VF')
f = findFont('RobotoDelta-VF')

print(f, f.axes)

def fitVariableWidth(varFont, s, w, fontSize, condensedLocation,
         wideLocation, fixedSize=False, tracking=None):
    """Answer the font instance that makes string s width on the given width
    *w* for the given *fontSize*. The *condensedLocation* dictionary defines
    the most condensed font instance (optionally including the opsz) and the
    *wideLocation* dictionary defines the most wide font instance (optionally
    including the opsz).

    The string width for s is calculated with both locations and then the
    [wdth] value is interpolated and iterated until the location is found where
    the string *s* fits width *w). Note that interpolation may not be enough,
    as the width axis may contain non-linear masters.  If the requested w
    outside of what is possible with two locations, then interations are
    performed to change the size. Again this cannot be done by simple
    interpolation, as the [opsz] also changes the width.  It one of the axes
    does not exist in the font, then use the default setting of the font."""

    condFont = getVarFontInstance(varFont, condensedLocation)
    condensedString = context.newString(s, style=dict(font=condFont.path,
        fontSize=fontSize, tracking=tracking, textFill=blackColor))
    condWidth, _ = condensedString.size
    wideFont = getVarFontInstance(varFont, wideLocation)
    wideString = context.newString(s, style=dict(font=wideFont.path, fontSize=fontSize,
        tracking=tracking, textFill=blackColor))
    wideWidth, _ = wideString.size

    # Check if the requested with is inside the boundaries of the font width
    # axis.
    if w < condWidth:
        font = condFont
        bs = condensedString
        location = condensedLocation
    elif w > wideWidth:
        font = wideFont
        bs = wideString
        location = wideLocation
    else:
        # Now interpolation the fitting location
        widthRange = wideLocation['wdth'] - condensedLocation['wdth']
        location = copy.copy(condensedLocation)
        location['wdth'] += widthRange*(w-condWidth)/(wideWidth-condWidth)
        font = getVarFontInstance(varFont, location)
        bs = c.newString(s, style=dict(font=font.path,
                                       fontSize=fontSize,
                                       tracking=tracking,
                                       textFill=blackColor))

    print(font, location)
    return dict(condensendFont=condFont,
                condensedString=condensedString,
                condWidth=condWidth,
                condensedLocation=condensedLocation,
                wideFont=wideFont,
                wideString=wideString,
                wideWidth=wideWidth,
                wideLocation=wideLocation,
                font=font,
                bs=bs,
                width=bs.size[0],
                location=location)

HEADLINE_SIZE = 36
HEADLINE = """When fonts started a new world."""


MIN_WDTH = f.axes['wdth'][0] # Minimum value of width [wdth] axis. 0 == Normal width
MAX_WDTH = f.axes['wdth'][2] # Maximum amount of compressions.
               # Larger value gives more condensed instance of
               # the Variable Font.
assert MIN_WDTH < MAX_WDTH

condensedLocation = dict(opsz=HEADLINE_SIZE,
                         wdth=MAX_WDTH,
                         wght=f.axes['wght'][1]) # Amount of condensed-ness > 0
wideLocation = dict(opsz=HEADLINE_SIZE,
                    wdth=MIN_WDTH,
                    wght=f.axes['wght'][1]) # Full default width = 0

W = 600
H = 220
Width = 200
PADDING = 20

INTERACTIVE = False # Interactive or save as animation.
FRAMES = 60

def draw(w):
    """Draw 3 lines of text: the boundaries of with the width axis 
    and the interpolated width from the slider value.
    If the slider goes of the extremes, then the middle line stops
    at the boundary width.
    """
    d = fitVariableWidth(f, HEADLINE, w, HEADLINE_SIZE,
                         condensedLocation, wideLocation)
    context.newPage(W, H)
    context.fill(1)
    context.rect(0, 0, W, H)
    context.text(d['condensedString'], (PADDING, 50))
    context.text(d['bs'], (PADDING, 100))
    context.text(d['wideString'], (PADDING, 150))
    context.fill(None)
    context.stroke(0)
    context.line((PADDING, PADDING), (PADDING, H-PADDING))
    context.line((PADDING+d['condWidth'], PADDING),
         (PADDING+d['condWidth'], H-PADDING))
    context.line((PADDING+d['width'], PADDING),
         (PADDING+d['width'], H-PADDING))
    context.line((PADDING+d['wideWidth'], PADDING),
         (PADDING+d['wideWidth'], H-PADDING))
    context.stroke(None)
    context.fill(0)
    context.text('%d %0.2f' % (round(d['condWidth']),
                         d['condensedLocation']['wdth']),
           (PADDING + d['condWidth'] + 5, PADDING))
    context.text('%d %0.2f' % (round(d['width']), d['location']['wdth']),
           (PADDING + d['width'] + 5, PADDING))
    context.text('%d %0.2f' % (round(d['wideWidth']), d['wideLocation']['wdth']),
           (PADDING + d['wideWidth'] + 5, PADDING))
    context.stroke((1, 0, 0))
    context.line((PADDING+w, PADDING), (PADDING+w, H-PADDING))
    context.stroke(None)
    #c.fill(1, 0, 0)
    context.text('Column %d' % w, (PADDING+w+5, H-PADDING-5))


angle = 0
while angle < 360:
    dx = sin(radians(angle)) * 0.5 + 0.5
    draw(160 + (W-2*PADDING-160) * dx)
    angle += 360/FRAMES
context.saveImage('_export/FitVariableHeadline.gif')

