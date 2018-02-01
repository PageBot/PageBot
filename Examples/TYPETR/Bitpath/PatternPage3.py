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
#     BitcountReference.py
#
#     This script the PDF document with Bitcount refernce information.
#
from math import sin, cos, pi
import pagebot
from pagebot.contexts import defaultContext as context
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot.contributions.filibuster.blurb import blurb
from pagebot.toolbox.transformer import path2ScriptId

if __name__ == '__main__':

    scriptGlobals = pagebot.getGlobals(path2ScriptId(__file__))

    #for k in sorted(getFamilyFontPaths('Bitpath')):
    #    print k

    if not hasattr(scriptGlobals, 'initialized'):
        scriptGlobals.initialized = True
        scriptGlobals.s1 = blurb.getBlurb('article_content', noTags=True)
        scriptGlobals.s2 = blurb.getBlurb('article_content', noTags=True)
        scriptGlobals.s3 = blurb.getBlurb('article_content', noTags=True)
        scriptGlobals.s4 = blurb.getBlurb('article_content', noTags=True)
        scriptGlobals.s5 = blurb.getBlurb('article_content', noTags=True)

    F = 50
    R = 10
    x = y = 20

    rLeading = 0.6

    for angle in range(0, 360, 10):
        context.newPage(1000, 1000)
        dx = sin(angle/360*2*pi) * R
        dy = cos(angle/360*2*pi) * R
        fs = context.newString(scriptGlobals.s1,
                               style=dict(font='BitpathGridDouble-RegularLineSquare',
                                          fontSize=F,
                                          textFill=(1, 0, 0),
                                          rLeading=rLeading))
        context.textBox(fs, (x, y, 1000, 900))

        fs = context.newString(scriptGlobals.s2,
                               style=dict(font='BitpathGridDouble-RegularLineSquare',
                                          fontSize=F,
                                          textFill=(0, 1, 0),
                                          rLeading=rLeading))
        context.textBox(fs, (x+7, y+7, 1000, 900))

        fs = context.newString(scriptGlobals.s3,
                               style=dict(font='BitpathGridDouble-RegularLineSquare',
                                          fontSize=F,
                                          textFill=(0, 1, 1),
                                          rLeading=rLeading))
        context.textBox(fs, (x, y+7, 1000, 900))

        fs = context.newString(scriptGlobals.s4,
                               style=dict(font='BitpathGridDouble-RegularLineSquare',
                                          fontSize=F,
                                          textFill=(1, 1, 0),
                                          rLeading=rLeading))
        context.textBox(fs, (x+7, y, 1000, 900))

        fs = context.newString(scriptGlobals.s5,
                               style=dict(font='BitpathGridDouble-BlackLineRound',
                                          fontSize=F,
                                          textFill=(0, 0, 0, 0.4),
                                          rLeading=rLeading))
        context.textBox(fs, (x+(-dx+dy)/2, y+(-dx+dy)/2, 1000, 900))

        fs = context.newString(scriptGlobals.s5,
                               style=dict(font='BitpathGridDouble-Round',
                                          fontSize=F,
                                          textFill=0,
                                          rLeading=rLeading))
        context.textBox(fs, (x+dx, y+dy, 1000, 900))

        fs = context.newString(scriptGlobals.s5,
                               style=dict(font='BitpathGridDouble-BookRound',
                                          fontSize=F,
                                          textFill=1,
                                          rLeading=rLeading))
        context.textBox(fs, (x+dx-2, y+dy+2, 1000, 900))
        
    context.saveImage('_export/PatternRotatingText.gif')
        
