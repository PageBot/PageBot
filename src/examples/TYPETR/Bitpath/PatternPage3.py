# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     BitcountReference.py
#
#     This script the PDF document with Bitcount refernce information.
#
import pagebot
from pagebot import getFormattedString
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot.contributions.filibuster.blurb import blurb

import myglobals

#for k in sorted(getFamilyFontPaths('Bitpath')):
#    print k

if not hasattr(myglobals, 'initialized'):
    myglobals.initialized = True
    myglobals.s1 = blurb.getBlurb('article_content', noTags=True)
    myglobals.s2 = blurb.getBlurb('article_content', noTags=True)
    myglobals.s3 = blurb.getBlurb('article_content', noTags=True)
    myglobals.s4 = blurb.getBlurb('article_content', noTags=True)
    myglobals.s5 = blurb.getBlurb('article_content', noTags=True)

F = 50
R = 10
x = y = 20

rLeading = 0.6

for angle in range(0, 360, 10):
    newPage(1000, 1000)
    dx = sin(angle/360*2*pi) * R
    dy = cos(angle/360*2*pi) * R
    fs = getFormattedString(myglobals.s1, None, ict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(1, 0, 0), rLeading=rLeading))
    textBox(fs, (x, y, 1000, 900))

    fs = getFormattedString(myglobals.s2, None, dict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(0, 1, 0), rLeading=rLeading))
    textBox(fs, (x+7, y+7, 1000, 900))

    fs = getFormattedString(myglobals.s3, None, dict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(0, 1, 1), rLeading=rLeading))
    textBox(fs, (x, y+7, 1000, 900))

    fs = getFormattedString(myglobals.s4, None, dict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(1, 1, 0), rLeading=rLeading))
    textBox(fs, (x+7, y, 1000, 900))

    fs = getFormattedString(myglobals.s5, None, dict(font='BitpathGridDouble-BlackLineRound', fontSize=F, textFill=(0, 0, 0, 0.4), rLeading=rLeading))
    textBox(fs, (x+(-dx+dy)/2, y+(-dx+dy)/2, 1000, 900))

    fs = getFormattedString(myglobals.s5, None, dict(font='BitpathGridDouble-Round', fontSize=F, textFill=0, rLeading=rLeading))
    textBox(fs, (x+dx, y+dy, 1000, 900))

    fs = getFormattedString(myglobals.s5, None, dict(font='BitpathGridDouble-BookRound', fontSize=F, textFill=1, rLeading=rLeading))
    textBox(fs, (x+dx-2, y+dy+2, 1000, 900))
    
saveImage('_export/PatternRotatingText.gif')
    