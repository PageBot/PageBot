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
#     PrintFontAxisInfo.py
#
import pagebot
from pagebot.fonttoolbox.objects.font import Font, AXES
from pagebot.fonttoolbox.variablefontbuilder import getVariableFont

FONT_PATH = pagebot.getFontPath()
fontPath = FONT_PATH + 'fontbureau/AmstelvarAlpha-VF.ttf'

def printFontInfo(aFont):
    print '-'*80
    print 'Family name', aFont.info.familyName
    print 'Style name', aFont.info.styleName
    print 'Number of glyphs', len(font)
    if aFont.axes:
        print 'Number of axes', len(aFont.axes)
        for axisTag, axisValues in sorted(aFont.axes.items()):
            print '\t' + axisTag, axisValues, 
            if axisTag in AXES:
                print AXES[axisTag]['name'], AXES[axisTag]['description']
            else:
                print 'Unknown axis'
    else:
        print'No Variable axes. This is a non-Variable font or an Variable instance.'

# Usage of PageBot Font class.
font = Font(fontPath)
printFontInfo(font)            
# Create an instance
instance = getVariableFont(font, dict(wdth=500, wght=200))
printFontInfo(instance)