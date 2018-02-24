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
#     Demo version of
#       pagebot.fonttoolbox.variablefontbuilder.fitVariableWidth
#     to show usage and format of the answered dictionary.
#
#     For real use, import the function as:
#     from pagebot.fonttoolbox.variablefontbuilder import fitVariableWidth
#
import copy
from math import sin, radians
from pagebot.contexts import defaultContext as c
from pagebot.contexts.platform import getRootFontPath
from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont

FONT_PATH = getRootFontPath() + '/fontbureau/AmstelvarAlpha-VF.ttf'
f = Font(FONT_PATH, install=True) # Get PageBot Font instance of Variable font.

def fitVariableWidth(varFont, s, w,
                     fontSize, condensedLocation,
                     wideLocation, fixedSize=False,
                     tracking=None, rTracking=None):
    u"""
      Answer the font instance that makes string s width on the given
       width *w* for the given *fontSize*.
      The *condensedLocation* dictionary defines the most condensed font
       instance (optionally including the opsz) and the *wideLocation*
       dictionary defines the most wide font instance (optionally including
       the opsz).
      The string width for s is calculated with both locations and then
       the [wdth] value is interpolated and iterated until the location is
       found where the string *s* fits width *w). Note that interpolation
       may not be enough, as the width axis may contain non-linear masters.
      If the requested w outside of what is possible with two locations,
       then interations are performed to change the size. Again this cannot
       be done by simple interpolation, as the [opsz] also changes the width.
      It one of the axes does not exist in the font, then use the default
       setting of the font.
    """
    condFont = getVariableFont(varFont, condensedLocation)
    condensedFs = c.newString(s, style=dict(font=condFont.installedName,
                                            fontSize=fontSize,
                                            tracking=tracking,
                                            rTracking=rTracking,
                                            textFill=0))
    condWidth, _ = c.textSize(condensedFs)
    wideFont = getVariableFont(varFont, wideLocation)

    wideFs = c.newString(s, style=dict(font=wideFont.installedName,
                                       fontSize=fontSize,
                                       tracking=tracking,
                                       rTracking=rTracking,
                                       textFill=0))
    wideWidth, _ = c.textSize(wideFs)
    # Check if the requested with is inside the boundaries of the font width axis
    if w < condWidth:
        font = condFont
        fs = condensedFs
        location = condensedLocation
    elif w > wideWidth:       
        font = wideFont
        fs = wideFs
        location = wideLocation
    else:
        # Now interpolation the fitting location
        widthRange = wideLocation['wdth'] - condensedLocation['wdth'] 
        location = copy.copy(condensedLocation)
        location['wdth'] += widthRange*(w-condWidth)/(wideWidth-condWidth)
        font = getVariableFont(varFont, location)
        fs = c.newString(s, style=dict(font=font.installedName,
                                       fontSize=fontSize,
                                       tracking=tracking,
                                       rTracking=rTracking,
                                       textFill=0))
    return dict(condensendFont=condFont,
                condensedFs=condensedFs,
                condWidth=condWidth,
                condensedLocation=condensedLocation,
                wideFont=wideFont,
                wideFs=wideFs,
                wideWidth=wideWidth,
                wideLocation=wideLocation,
                font=font,
                fs=fs,
                width=c.textSize(fs)[0],
                location=location)

HEADLINE_SIZE = 36
HEADLINE = """When fonts started a new world."""


MIN_WDTH = 0 # Minimum value of width [wdth] axis. 0 == Normal width
MAX_WDTH = 0.8 # Maximum amount of compressions.
               # Larger value gives more condensed instance of
               # the Variable Font.
assert MIN_WDTH < MAX_WDTH

condensedLocation = dict(opsz=HEADLINE_SIZE,
                         wdth=MAX_WDTH,
                         wght=0.7) # Amount of condensed-ness > 0
wideLocation = dict(opsz=HEADLINE_SIZE,
                    wdth=MIN_WDTH,
                    wght=0.7) # Full default width = 0

W = 600
H = 220
Width = 200
PADDING = 20

INTERACTIVE = False # Interactive or save as animation.
FRAMES = 60

def draw(w):
    u"""
      Draw 3 lines of text: the boundaries of with the width axis
       and the interpolated width from the slider value.
      If the slider goes of the extremes, then the middle line stops
       at the boundary width.
    """
    d = fitVariableWidth(f, HEADLINE, w, HEADLINE_SIZE,
                         condensedLocation, wideLocation)

    c.newPage(W, H)
    c.fill(1)
    c.rect(0, 0, W, H)
    c.text(d['condensedFs'], (PADDING, 50))
    c.text(d['fs'], (PADDING, 100))
    c.text(d['wideFs'], (PADDING, 150))
    c.fill(None)
    c.stroke(0)
    c.line((PADDING, PADDING), (PADDING, H-PADDING))
    c.line((PADDING+d['condensedWidth'], PADDING),
         (PADDING+d['condensedWidth'], H-PADDING))
    c.line((PADDING+d['width'], PADDING),
         (PADDING+d['width'], H-PADDING))
    c.line((PADDING+d['wideWidth'], PADDING),
         (PADDING+d['wideWidth'], H-PADDING))
    c.stroke(None)
    c.fill(0)
    c.text('%d %0.2f' % (round(d['condensedWidth']),
                         d['condensedLocation']['wdth']),
           (PADDING + d['condensedWidth'] + 5, PADDING))
    c.text('%d %0.2f' % (round(d['width']), d['location']['wdth']),
           (PADDING + d['width'] + 5, PADDING))
    c.text('%d %0.2f' % (round(d['wideWidth']), d['wideLocation']['wdth']),
           (PADDING + d['wideWidth'] + 5, PADDING))
    c.stroke(1, 0, 0)
    c.line((PADDING+w, PADDING), (PADDING+w, H-PADDING))
    c.stroke(None)
    c.fill(1, 0, 0)
    c.text('Column %d' % w, (PADDING+w+5, H-PADDING-5))

if INTERACTIVE:
    #dict(name='ElementOrigin', ui='CheckBox', args=dict(value=False)),
    c.Variable(
        [dict(name='Width',
              ui='Slider',
              args=dict(minValue=PADDING,
                        value=200,
                        maxValue=W-2*PADDING))
        ], globals())

    draw(Width)
else:
    angle = 0
    while angle < 360:
        dx = sin(radians(angle)) * 0.5 + 0.5
        draw(160 + (W-2*PADDING-160) * dx)
        angle += 360/FRAMES
    c.saveImage('_export/fitVariableHeadline.gif')

