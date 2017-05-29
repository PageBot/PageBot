# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     PrintAxisInfo.py
#
from __future__ import division

import pagebot
from pagebot.fonttoolbox.objects.font import Font, AXES

fontPath = pagebot.getFontPath() + 'fontbureau/AmstelvarAlpha-VF.ttf'
#fontPath = pagebot.getFontPath() + 'fontbureau/Decovar-VF_2017-02-06.ttf'
font = Font(fontPath)
print 'Family name', font.info.familyName
print 'Style name', font.info.styleName
print 'Number of glyphs', len(font)
if font.axes:
    print 'Number of axes', len(font.axes)
    for axisTag, axisValues in sorted(font.axes.items()):
        print '\t' + axisTag, axisValues, 
        if axisTag in AXES:
            print AXES[axisTag]['name'], AXES[axisTag]['description']
        else:
            print 'Unknown axis'
else:
    print'No Variable axes.'
            
        