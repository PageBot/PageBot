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
#     testGlyphAnalyzer.py
#
from pagebot.fonttoolbox.objects.font import Font
from pagebot.fonttoolbox.analyzers.glyphanalyzer import GlyphAnalyzer
from pagebot.toolbox.color import color

EXPORT_PATH = '_export/testGlyphAnalyzer.pdf'

FONT_PATH = '/Library/Fonts/'
paths = [   
    FONT_PATH+'Verdana Bold.ttf',
    FONT_PATH+'Verdana.ttf',   
    FONT_PATH+'Georgia Bold.ttf',
    FONT_PATH+'Georgia.ttf',   
]
for path in paths:
    font = Font(path)
    EM = font.info.unitsPerEm
    gaH = GlyphAnalyzer(font['H'])

    for gName in ('H', 'O'):
        newPage(EM, EM)
        translate(100, -font.info.descender)
    
        fontSize(24)
        text(path, (0, -EM/20))
    
        ga = GlyphAnalyzer(font[gName])
        #print(ga.glyph.points)
        #for contour in ga.glyph.flattenedPathPoints:
        #    print('===Contour')
        #    for p in contour:
        #        print('    %s' % p)
        line = (-10000, 400), (10000, 400)
        print(ga.intersectWithLine(line))
        
        strokeWidth(3)
        stroke(0.6)
        fill(0.92)
        drawPath(ga.glyph.path)
    
        # Horizontal lines
        strokeWidth(1)
        stroke(0, 0, 1)
        line((0, ga.minY), (ga.width, ga.minY))
        line((0, ga.maxY), (ga.width, ga.maxY))
    
        # H-metrics
        line((0, gaH.maxY), (ga.width, gaH.maxY))
        line((0, gaH.minY), (ga.width, gaH.minY))
        line((0, 0), (ga.width, 0))

        line((0, 0), (0, gaH.maxY))
        line((0, 0), (0, gaH.maxY))
    
    
        # Verticals
        prevX = 0
        verticalX = ga.verticals.keys() + [ga.width]
        for x in sorted(verticalX):
            strokeWidth(1)
            stroke(0, 0, 1)
            line((x, ga.minY), (x, ga.maxY))
            stroke(None)
            fill(0.5)
            fs = FormattedString('%d' % round(x - prevX), fontSize=20, fill=color(0.5)
            tw, th = textSize(fs)
            text(fs, (prevX + (x-prevX)/2 - tw/2, -th/2-50))
            prevX = x
        
saveImage(EXPORT_PATH)
